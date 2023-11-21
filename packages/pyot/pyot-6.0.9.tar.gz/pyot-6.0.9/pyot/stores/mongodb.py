import datetime
from typing import Any
import pytz

import motor.motor_asyncio as mongo
from pyot.core.exceptions import NotFound
from pyot.pipeline.token import PipelineToken
from pyot.pipeline.expiration import ExpirationManager
from pyot.core.resources import ResourceTemplate
from pyot.utils.logging import LazyLogger

from .base import Store, StoreType


LOGGER = LazyLogger(__name__)


class MongoDB(Store):

    type = StoreType.CACHE

    def __init__(self, game: str, db: str, host='127.0.0.1', port=27017, expirations: Any = None, log_level: int = 0, **kwargs) -> None:
        self.game = game
        if 'connect' not in kwargs:
            kwargs['connect'] = False
        if 'w' not in kwargs:
            kwargs['w'] = 0
        self.db = db
        self.initialized = False
        self.mongos = ResourceTemplate(
            acquire_func=lambda: self.acquire_database(host=host, port=port, **kwargs),
            release_func=lambda database: database.client.close()
        )
        self.location = f"{host}:{port}:{db}"
        self.expirations = ExpirationManager(game, expirations)
        self.log_level = log_level

    async def acquire_database(self, host: str, port: int, **kwargs):
        database = mongo.AsyncIOMotorClient(host=host, port=port, **kwargs)[self.db]
        for method in self.expirations:
            indexes = await database[method].index_information()
            if 'setAt_1' in indexes:
                if self.expirations.get_timeout(method) >= 0:
                    await database.command('collMod', method, index={'keyPattern': {'setAt': 1}, 'expireAfterSeconds': self.expirations.get_timeout(method)})
                else:
                    await database[method].drop_index('setAt')
            elif self.expirations.get_timeout(method) > 0:
                await database[method].create_index('token')
                await database[method].create_index('setAt', expireAfterSeconds=self.expirations.get_timeout(method))
            else:
                await database[method].create_index('token')
        return database

    async def set(self, token: PipelineToken, value: Any, **kwargs) -> None:
        timeout = self.expirations.get_timeout(token.method)
        if timeout != 0:
            cache = await self.mongos.acquire()
            await cache[token.method].insert_one(
                {
                    'token': token.value,
                    'data': value,
                    'dataType': "bson",
                    'setAt': datetime.datetime.now(pytz.utc)
                }
            )
            LOGGER.log(self.log_level, f"[pyot.stores.mongodb:MongoDB#{self.location}] SET {token.value}")

    async def get(self, token: PipelineToken, **kwargs) -> Any:
        timeout = self.expirations.get_timeout(token.method)
        if timeout == 0:
            raise NotFound(token.value)
        cache = await self.mongos.acquire()
        item = await cache[token.method].find_one({'token': token.value})
        if item is None:
            raise NotFound(token.value)
        LOGGER.log(self.log_level, f"[pyot.stores.mongodb:MongoDB#{self.location}] GET {token.value}")
        if item.get("dataType", None) is None:
            await cache[token.method].delete_many({'token': token.value})
            raise NotFound(token.value)
        return item["data"]

    async def delete(self, token: PipelineToken, **kwargs) -> None:
        cache = await self.mongos.acquire()
        await cache[token.method].delete_many({'token': token.value})
        LOGGER.log(self.log_level, f"[pyot.stores.mongodb:MongoDB#{self.location}] DELETE {token.value}")

    async def contains(self, token: PipelineToken, **kwargs) -> bool:
        cache = await self.mongos.acquire()
        item = await cache[token.method].find_one({'token': token.value})
        if item is None:
            return False
        return True

    async def clear(self, **kwargs):
        cache = await self.mongos.acquire()
        collections = await cache.list_collection_names()
        for name in collections:
            await cache.drop_collection(name)
        LOGGER.log(self.log_level, f"[pyot.stores.mongodb:MongoDB#{self.location}] Store cleared successfully")

import datetime
from typing import Any
import pickle
import copy

from pyot.utils.threading import AsyncLock
from pyot.core.exceptions import NotFound
from pyot.pipeline.token import PipelineToken
from pyot.pipeline.expiration import ExpirationManager
from pyot.utils.logging import LazyLogger

from .base import Store, StoreType


LOGGER = LazyLogger(__name__)


class Omnistone(Store):

    type = StoreType.CACHE

    def __init__(self, game: str, max_entries: int = 10000, cull_frecuency: int = 2, expirations: Any = None, log_level: int = 0) -> None:
        self._lock = AsyncLock()
        self._cull_lock = [False, datetime.datetime.now()]
        self.game = game
        self.data = dict()
        self.expirations = ExpirationManager(game, expirations)
        self.max_entries = max_entries
        self.cull_frecuency = cull_frecuency
        self.log_level = log_level

    async def set(self, token: PipelineToken, value: Any, **kwargs) -> None:
        timeout = self.expirations.get_timeout(token.method)
        if timeout != 0:
            async with self._lock:
                if timeout != -1:
                    timeout = datetime.timedelta(seconds=timeout)
                if await self._allowed():
                    value = pickle.dumps(value)
                    self.data[token.value] = (value, timeout, datetime.datetime.now(), datetime.datetime.now())
                    LOGGER.log(self.log_level, f"[pyot.stores.omnistone:Omnistone] SET {token.value}")
            if len(self.data) > self.max_entries and await self._allowed():
                async with self._lock:
                    self._cull_lock = [True, datetime.datetime.now()]
                await self.expire()
                if len(self.data) > self.max_entries - self.max_entries/self.cull_frecuency:
                    await self.cull()

    async def get(self, token: PipelineToken, expiring: bool = False, **kwargs) -> Any:
        timeout = self.expirations.get_timeout(token.method)
        if timeout == 0:
            raise NotFound(token.value)
        async with self._lock:
            try:
                item, timeout, entered, _ = self.data[token.value]
            except KeyError as e:
                raise NotFound(token.value) from e
            if not expiring:
                LOGGER.log(self.log_level, f"[pyot.stores.omnistone:Omnistone] GET {token.value}")

            now = datetime.datetime.now()
            if timeout == -1:
                self.data[token.value] = (item, timeout, entered, now)
                item = pickle.loads(item)
                return item
            elif now > entered + timeout:
                try:
                    del self.data[token.value]
                except KeyError: pass
                raise NotFound(token.value)
            else:
                self.data[token.value] = (item, timeout, entered, now)
                item = pickle.loads(item)
                return item

    async def delete(self, token: PipelineToken, **kwargs) -> None:
        try:
            del self.data[token.value]
            LOGGER.log(self.log_level, f"[pyot.stores.omnistone:Omnistone] DELETE {token.value}")
        except KeyError as e:
            raise NotFound(token.value) from e

    async def expire(self, **kwargs):
        for token in self.data:
            await self.get(token, expiring=True)

    async def clear(self, **kwargs):
        async with self._lock:
            self.data = {}
            LOGGER.log(self.log_level, f"[pyot.stores.omnistone:Omnistone] Store cleared successfully")

    async def _allowed(self):
        if not self._cull_lock[0]:
            return True
        elif self._cull_lock[0] and datetime.datetime.now() > self._cull_lock[1] + datetime.timedelta(seconds=30):
            self._cull_lock[0] = False
            return True
        else:
            return False

    async def cull(self):
        async with self._lock:
            data = copy.copy(self.data)
        lru = sorted(data.keys(), key=lambda x: data[x][3])
        for token in lru[:int(len(data)/self.cull_frecuency)]:
            await self.delete(token)
        self._cull_lock[0] = False

    async def contains(self, token: PipelineToken, **kwargs) -> bool:
        try:
            _ = self.data[token.value]
            return True
        except KeyError:
            return False

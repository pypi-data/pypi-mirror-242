from pyot.conf.model import models
from pyot.core.functional import empty
from .base import PyotCore


class Account(PyotCore):
    puuid: str
    game_name: str
    tag_line: str

    class Meta(PyotCore.Meta):
        rules = {
            "account_v1_by_puuid": ["puuid"],
            "account_v1_by_riot_id": ["game_name", "tag_line"],
        }

    def __init__(self, puuid: str = empty, game_name: str = empty, tag_line: str = empty, region: str = models.riot.DEFAULT_REGION):
        self.initialize(locals())

    def active_shard(self, game: str):
        return ActiveShard(puuid=self.puuid, game=game).using(self.metapipeline.name)


class ActiveShard(PyotCore):
    puuid: str
    game: str
    active_shard: str

    class Meta(PyotCore.Meta):
        rules = {"account_v1_active_shard": ["puuid", "game"]}

    def __init__(self, puuid: str = empty, game: str = empty, region: str = models.riot.DEFAULT_REGION):
        self.initialize(locals())

    @property
    def platform(self):
        try:
            return self.active_shard
        except AttributeError:
            return super().platform

    @property
    def account(self):
        return Account(puuid=self.puuid)

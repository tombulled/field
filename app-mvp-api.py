from typing import Any

from meta import MetadataManager


class StaticMetadataManager(MetadataManager[Any, str]):
    def resolve(self, value, metadata):
        return "static!"


m = "some metadata"
v = "some value"
mm = StaticMetadataManager()
r = mm.resolve(v, m)

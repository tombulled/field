from typing import Any, Mapping, Type

from . import metadata, resolvers
from .errors import ResolutionError
from .typing import Metadata

# TODO: Type value type (instead of `Any`)
RESOLVERS: Mapping[Type[Metadata], Any] = {
    metadata.Gt: resolvers.gt,
}


def resolve(meta: Metadata, value: Any) -> Any:
    for meta_cls, resolver in RESOLVERS.items():
        if issubclass(type(meta), meta_cls):
            return resolver(meta, value)

    raise ResolutionError

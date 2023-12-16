from dataclasses import dataclass
from typing import Any

from meta.api import ResolverGroup

"""
Standard Metadata Resolution Strategies:
    1. Parsing - replaces the value with the result of resolution
        E.g: resolve(Suffix("!"), "foo") == "foo!"
    2. Validation - does something with the result of resolution
    3. NoOp - does nothing with the result of resolution

The "parsing" strategy (aka piping the new value, onioning) fits all:
    1. Parsing - resolution result replaces value
    2. Validation - exception thrown, or original value returned
    3. NoOp - original value returned
"""


class AnnotatedTypesManager(MetadataManager[BaseMetadata,]):
    _resolvers = {}


# class PydanticMetadataManager(MetadataManager[BaseModel, ]):


@dataclass
class Prefix:
    prefix: str

    def resolve(self, value: Any, /) -> str:
        return self.prefix + str(value)


@dataclass
class Suffix:
    suffix: str

    def resolve(self, value: Any, /) -> str:
        return str(value) + self.suffix


rg = ResolverGroup(
    {
        Prefix: Prefix.resolve,
        Suffix: Suffix.resolve,
    }
)

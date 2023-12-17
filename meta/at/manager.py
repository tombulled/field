from typing import Any, Optional, TypeVar

from annotated_types import BaseMetadata

from ..api import MetadataManager
from ..resolver import Resolvers
from . import metadata, resolvers
from .errors import ValidationError

__all__ = ("AnnotatedTypes",)

T = TypeVar("T")


RESOLVERS: Resolvers[Any, bool] = {
    metadata.Gt: resolvers.check_gt,
    metadata.Ge: resolvers.check_ge,
    metadata.Lt: resolvers.check_lt,
    metadata.Le: resolvers.check_le,
    metadata.MultipleOf: resolvers.check_multiple_of,
    metadata.MinLen: resolvers.check_min_len,
    metadata.MaxLen: resolvers.check_max_len,
    metadata.Timezone: resolvers.check_timezone,
    metadata.Predicate: resolvers.check_predicate,
}


class AnnotatedTypes(MetadataManager[BaseMetadata, Any]):
    resolvers: Resolvers[Any, bool]

    def __init__(self, resolvers: Optional[Resolvers[Any, bool]] = None) -> None:
        if resolvers is not None:
            self.resolvers = resolvers
        else:
            self.resolvers = RESOLVERS

    def __repr__(self) -> str:
        return f"{type(self).__name__}({hex(hash(self))})"

    def resolve(self, meta: BaseMetadata, value: T, /) -> T:
        resolution: Optional[bool] = None

        try:
            resolution = self.check(meta, value)
        except Exception as error:
            self.on_error(meta, value, error)

        if resolution is not None:
            if resolution:
                self.on_pass(meta, value)
            else:
                self.on_fail(meta, value)

        return value

    def check(self, meta: BaseMetadata, value: Any, /) -> bool:
        return super().resolve(meta, value)

    def on_pass(self, meta: BaseMetadata, value: Any) -> None:
        pass

    def on_fail(self, meta: BaseMetadata, value: Any) -> None:
        raise ValidationError(f"Value {value!r} failed constraint {meta!r}")

    def on_error(self, meta: BaseMetadata, value: Any, error: Exception) -> None:
        raise error

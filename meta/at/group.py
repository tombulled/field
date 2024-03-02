from typing import Any, TypeVar

from annotated_types import BaseMetadata
from meta.api import Resolver
from meta.at.errors import ValidationError
from meta.group import ResolverGroup
from meta.at import metadata, resolvers

T = TypeVar("T")

RESOLVERS: ResolverGroup[Any, bool] = ResolverGroup(
    {
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
)


class AnnotatedTypes(Resolver[BaseMetadata, Any]):
    resolvers: ResolverGroup[Any, bool] = RESOLVERS

    def __repr__(self) -> str:
        return f"{type(self).__name__}({hex(hash(self))})"

    def __call__(self, metadata: BaseMetadata, value: T, /) -> T:
        validated: bool = self.resolvers.resolve(metadata, value)

        if not validated:
            raise ValidationError(f"Value {value!r} failed constraint {metadata!r}")

        return value


AT = AnnotatedTypes()

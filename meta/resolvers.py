from typing import Any, TypeVar

from .errors import ResolutionError
from .metadata import Gt, Lt
from .resolver import ResolversMap
from .types import SupportsGt, SupportsLt
from .typing import Metadata

T = TypeVar("T")

RESOLVERS: ResolversMap[Metadata, Any] = ResolversMap()

# TODO: Rename `resolve` to  apply / validate / implement / check / handle / consume / parse?


@RESOLVERS(Gt)
def gt(meta: Gt, value: T) -> T:
    if not isinstance(value, SupportsGt):
        raise TypeError(f"The 'gt' constraint cannot be applied to {type(value)}")

    if not value > meta.gt:
        raise ResolutionError(f"Input should be greater than {meta.gt}")

    return value


@RESOLVERS(Lt)
def lt(meta: Lt, value: T) -> T:
    if not isinstance(value, SupportsLt):
        raise TypeError(f"The 'lt' constraint cannot be applied to {type(value)}")

    if not value < meta.lt:
        raise ResolutionError(f"Input should be less than {meta.lt}")

    return value


# Gt (done)
# Ge
# Lt (done)
# Le
# Interval
# MultipleOf
# MinLen
# MaxLen
# Len
# Timezone
# Predicate
# Doc

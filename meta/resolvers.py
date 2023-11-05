from typing import Any
from .resolver import ResolversMap
from .errors import ResolutionError
from .types import SupportsGt
from .typing import Metadata
from .metadata import Gt

RESOLVERS: ResolversMap[Metadata, Any] = ResolversMap()

# resolve / apply / validate / implement / check / handle / consume / parse
@RESOLVERS(Gt)
def gt(meta, value) -> None:
    if not isinstance(value, SupportsGt):
        raise TypeError(f"The 'gt' constraint cannot be applied to {type(value)}")

    if not value > meta.gt:
        raise ResolutionError(f"Input should be greater than {meta.gt}")


# Ge
# Lt
# Le
# Interval
# MultipleOf
# MinLen
# MaxLen
# Len
# Timezone
# Predicate
# Doc

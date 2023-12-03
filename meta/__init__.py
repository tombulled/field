from .base import BaseMetadata, GroupedMetadata
from .errors import ResolutionError
from .manager import Meta
from .metadata import *
from .params import Params
from .resolvers import *

METAS = Meta(
    {
        # Gt: resolve_gt,
        # Ge: resolve_ge,
        # Lt: resolve_lt,
        # Le: resolve_le,
        # Gt: check_gt,
        # Ge: check_ge,
        # Lt: check_lt,
        # Le: check_le,
        # MultipleOf: resolve_multiple_of,
        # MinLen: resolve_min_len,
        # MaxLen: resolve_max_len,
        # Timezone: resolve_timezone,
        # Predicate: resolve_predicate,
    }
)
PARAMS = Params(METAS)

resolve = METAS.resolve
wrap = PARAMS.wrap

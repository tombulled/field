from .base import BaseMetadata, GroupedMetadata
from .errors import ResolutionError
from .manager import Metas
from .metadata import *
from .params import Params
from .resolvers import RESOLVERS

METAS = Metas(RESOLVERS)
PARAMS = Params(METAS)

resolve = METAS.resolve
wrap = PARAMS.wrap

from .api import resolve
from .base import BaseMetadata, GroupedMetadata
from .errors import ResolutionError
from .manager import Metas
from .metadata import *
from .resolvers import RESOLVERS

MANAGER = Metas(RESOLVERS)

resolve = MANAGER.resolve

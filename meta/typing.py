import sys
from typing import Union

if sys.version_info < (3, 9):
    from typing_extensions import Annotated
else:
    from typing import Annotated

from .base import BaseMetadata, GroupedMetadata

__all__ = (
    "Annotated",
    "Metadata",
)

Metadata = Union[BaseMetadata, GroupedMetadata]

import sys

if sys.version_info < (3, 9):
    from typing_extensions import Annotated
else:
    from typing import Annotated

from .base import BaseMetadata

__all__ = ("Annotated", "Metadata",)

Metadata = BaseMetadata

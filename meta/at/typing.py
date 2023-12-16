from typing import Union

from annotated_types import BaseMetadata, GroupedMetadata

__all__ = ("Metadata",)

Metadata = Union[BaseMetadata, GroupedMetadata]

import sys
from typing import Any, Iterator, Optional, Sequence, Tuple, Type

import annotated_types

if sys.version_info < (3, 9):
    from typing_extensions import Annotated, get_args, get_origin
else:
    from typing import Annotated, get_args, get_origin

__all__: Sequence[str] = ("get_metadata",)


def get_metadata(typ: Type[Any]) -> Iterator[Any]:
    origin: Optional[Any] = get_origin(typ)

    if origin is not Annotated:
        return

    metadatas: Sequence[Any]
    _, *metadatas = get_args(typ)

    for metadata in metadatas:
        if isinstance(metadata, annotated_types.BaseMetadata):
            yield metadata
        elif isinstance(metadata, annotated_types.GroupedMetadata):
            yield from metadata

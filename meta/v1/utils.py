import sys
from typing import Any, Iterator, Sequence

import annotated_types

if sys.version_info < (3, 9):
    from typing_extensions import Annotated, get_args, get_origin
else:
    from typing import Annotated, get_args, get_origin

__all__: Sequence[str] = ("get_metadata", "is_annotated", "get_annotated_type")

def new_get_metadata(tp: type) -> Iterator[Any]:
    origin = get_origin(tp)
    assert origin is Annotated
    args = iter(get_args(tp))
    next(args)
    for arg in args:
        if isinstance(arg, annotated_types.BaseMetadata):
            yield arg
        elif isinstance(arg, annotated_types.GroupedMetadata):
            yield from arg

def get_metadata(typ: Any, /) -> Sequence[Any]:
    if hasattr(typ, "__metadata__"):
        return typ.__metadata__

    return ()


def is_annotated(typ: Any, /) -> bool:
    return bool(get_metadata(typ))


def get_annotated_type(typ: Any, /) -> Any:
    if not is_annotated(typ):
        return typ

    return typ.__origin__

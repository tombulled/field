import typing
from typing import Any, Sequence

__all__: Sequence[str] = ("get_metadata", "is_annotated", "get_annotated_type")


def get_metadata(typ: Any, /) -> Sequence[Any]:
    if hasattr(typ, "__metadata__"):
        return typ.__metadata__

    return ()


def is_annotated(typ: Any, /) -> bool:
    return bool(get_metadata(typ))


def get_annotated_type(typ: Any, /) -> Any:
    if not is_annotated(typ):
        return typ

    return typing.get_origin(typ)

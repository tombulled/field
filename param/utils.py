import inspect
from typing import Any, Sequence

from .sentinels import Missing
from .typing import AnyOrMissing

__all__: Sequence[str] = ("empty_to_missing", "get_metadata", "is_annotated")


def empty_to_missing(value: Any, /) -> AnyOrMissing:
    if value is inspect.Parameter.empty:
        return Missing

    return value


def get_metadata(typ: Any, /) -> Sequence[Any]:
    if hasattr(typ, "__metadata__"):
        return typ.__metadata__

    return ()


def is_annotated(typ: Any, /) -> bool:
    return hasattr(typ, "__metadata__")

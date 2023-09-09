from typing import Any, Sequence

__all__: Sequence[str] = ("get_metadata", "is_annotated")


def get_metadata(typ: Any, /) -> Sequence[Any]:
    if hasattr(typ, "__metadata__"):
        return typ.__metadata__

    return ()


def is_annotated(typ: Any, /) -> bool:
    return hasattr(typ, "__metadata__")

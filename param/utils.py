import inspect
from typing import Any, Sequence

from .sentinels import Missing
from .typing import AnyOrMissing

__all__: Sequence[str] = ("parse_parameter_value", "get_metadata", "is_annotated")


# NOTE: Not just the parameter value, could also be the return type
def parse_parameter_value(value: Any, /) -> AnyOrMissing:
    if value is inspect.Parameter.empty:
        return Missing
    else:
        return value


def get_metadata(typ: Any, /) -> Sequence[Any]:
    if hasattr(typ, "__metadata__"):
        return typ.__metadata__

    return ()


def is_annotated(typ: Any, /) -> bool:
    return hasattr(typ, "__metadata__")

import inspect
from typing import Any, Sequence

from .sentinels import Undefined

__all__: Sequence[str] = ("parse_parameter_value",)


def parse_parameter_value(value: Any, /) -> Any:
    if value is inspect.Parameter.empty:
        return Undefined
    else:
        return value
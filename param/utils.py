import inspect
from typing import Any, Union

from .sentinels import Missing, MissingType


def parse(value: Any, /) -> Union[Any, MissingType]:
    if value is inspect.Parameter.empty:
        return Missing
    else:
        return value

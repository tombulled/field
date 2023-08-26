import inspect
from typing import Any, Sequence, Union

from pydantic.fields import Undefined, UndefinedType

__all__: Sequence[str] = ("parse",)


def parse(value: Any, /) -> Union[Any, UndefinedType]:
    if value is inspect.Parameter.empty:
        return Undefined
    else:
        return value

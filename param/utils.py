import inspect
from typing import Any, Union

from pydantic.fields import FieldInfo, Undefined, UndefinedType


def parse(value: Any, /) -> Union[Any, UndefinedType]:
    if value is inspect.Parameter.empty:
        return Undefined
    else:
        return value


def has_default(field: FieldInfo, /) -> bool:
    return field.default is not Undefined or field.default_factory is not None


def get_default(field: FieldInfo, /) -> Any:
    if field.default_factory is not None:
        return field.default_factory()
    else:
        return field.default

from typing import Callable, Union, TypeVar
from .sentinels import MissingType, Missing
from . import field

T = TypeVar("T")


def Field(
    *,
    default: Union[T, MissingType] = Missing,
    default_factory: Union[Callable[[], T], MissingType] = Missing
) -> field.Field:
    return field.Field(default=default, default_factory=default_factory)

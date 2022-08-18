from typing import Callable, Union, TypeVar
from .sentinels import MissingType, Missing
from . import param

T = TypeVar("T")


def Param(
    *,
    default: Union[T, MissingType] = Missing,
    default_factory: Union[Callable[[], T], MissingType] = Missing
) -> param.Param[T]:
    return param.Param(default=default, default_factory=default_factory)

from typing import Callable, TypeVar, Union

from . import parameters
from .sentinels import Missing, MissingType

T = TypeVar("T")


def Param(
    *,
    default: Union[T, MissingType] = Missing,
    default_factory: Union[Callable[[], T], MissingType] = Missing
) -> parameters.Param[T]:
    return parameters.Param(default=default, default_factory=default_factory)

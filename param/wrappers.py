from typing import Callable, TypeVar, Union

from . import models
from .sentinels import Missing, MissingType

T = TypeVar("T")


def Param(
    *,
    default: Union[T, MissingType] = Missing,
    default_factory: Union[Callable[[], T], MissingType] = Missing
) -> models.Param[T]:
    return models.Param(default=default, default_factory=default_factory)

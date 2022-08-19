from typing import Callable, Union, TypeVar
from .sentinels import MissingType, Missing
from .models import ParameterSpecification

T = TypeVar("T")


def Param(
    *,
    default: Union[T, MissingType] = Missing,
    default_factory: Union[Callable[[], T], MissingType] = Missing
) -> ParameterSpecification[T]:
    return ParameterSpecification(default=default, default_factory=default_factory)

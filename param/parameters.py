from abc import ABC
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar, Union

from .sentinels import Missing, MissingType

T = TypeVar("T")


class ParameterSpecification(ABC):
    pass


@dataclass(frozen=True)
class Param(Generic[T], ParameterSpecification):
    default: Union[T, MissingType] = Missing
    default_factory: Union[Callable[[], T], MissingType] = Missing

    def __post_init__(self):
        if self.default is not Missing and self.default_factory is not Missing:
            raise ValueError("cannot specify both `default` and `default_factory`")

    def get_default(self) -> Union[T, MissingType]:
        if self.default_factory is not Missing:
            return self.default_factory()
        elif self.default is not Missing:
            return self.default

        return Missing

    def has_default(self) -> bool:
        return self.default is not Missing or self.default_factory is not Missing

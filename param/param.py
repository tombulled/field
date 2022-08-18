from dataclasses import dataclass
from typing import Callable, Generic, NoReturn, TypeVar, Union
from .sentinels import Missing, MissingType


T = TypeVar("T")

@dataclass(init=False, repr=False)
class Param(Generic[T]):
    _default: Union[T, MissingType]
    _default_factory: Union[Callable[[], T], MissingType]

    def __init__(
        self,
        *,
        default: Union[T, MissingType] = Missing,
        default_factory: Union[Callable[[], T], MissingType] = Missing,
    ):
        if default is not Missing and default_factory is not Missing:
            raise ValueError("cannot specify both `default` and `default_factory`")

        self._default = default
        self._default_factory = default_factory

    def __repr__(self) -> str:
        if self._default_factory is not Missing:
            return f"{type(self).__name__}(default_factory={self._default_factory})"
        elif self._default is not Missing:
            return f"{type(self).__name__}(default={self._default})"

        return f"{type(self).__name__}()"

    @property
    def default(self) -> Union[T, NoReturn]:
        if self._default_factory is not Missing:
            return self._default_factory()
        elif self._default is not Missing:
            return self._default

        raise Exception("There is no default")

    def has_default(self) -> bool:
        return self._default is not Missing or self._default_factory is not Missing

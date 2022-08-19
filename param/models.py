from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Generic, NoReturn, Tuple, TypeVar, Union

from .enums import ParameterType
from .sentinels import Missing, MissingType

T = TypeVar("T")


@dataclass(init=False, repr=False)
class ParameterSpecification(Generic[T]):
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
            return f"{type(self).__name__}(default_factory={self._default_factory!r})"
        elif self._default is not Missing:
            return f"{type(self).__name__}(default={self._default!r})"

        return f"{type(self).__name__}()"

    @property
    def default(self) -> Union[T, MissingType]:
        if self._default_factory is not Missing:
            return self._default_factory()
        elif self._default is not Missing:
            return self._default

        return Missing

    def has_default(self) -> bool:
        return self._default is not Missing or self._default_factory is not Missing


@dataclass
class Arguments:
    args: Tuple[Any, ...] = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    arguments: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Parameter:
    name: str
    annotation: Any
    type: ParameterType
    spec: ParameterSpecification

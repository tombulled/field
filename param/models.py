import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Generic, Tuple, TypeVar, Union

from .enums import ParameterType
from .parameters import ParameterSpecification
from .sentinels import Missing, MissingType
from .utils import parse

T = TypeVar("T")
S = TypeVar("S", bound=ParameterSpecification)


@dataclass(frozen=True)
class Arguments:
    args: Tuple[Any, ...] = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)

    def call(self, func: Callable[..., T], /) -> T:
        return func(*self.args, **self.kwargs)


@dataclass(frozen=True)
class BoundArguments:
    args: Dict[str, Any] = field(default_factory=dict)
    kwargs: Dict[str, Any] = field(default_factory=dict)

    def call(self, func: Callable[..., T], /) -> T:
        return func(*self.args.values(), **self.kwargs)

    @property
    def arguments(self) -> Dict[str, Any]:
        return {**self.args, **self.kwargs}


@dataclass(frozen=True)
class Parameter:
    name: str
    default: Union[Any, MissingType] = Missing
    annotation: Union[Any, MissingType] = Missing
    type: ParameterType = ParameterType.POSITIONAL_OR_KEYWORD

    @classmethod
    def from_parameter(cls, parameter: inspect.Parameter, /) -> "Parameter":
        return cls(
            name=parameter.name,
            default=parse(parameter.default),
            annotation=parse(parameter.annotation),
            type=ParameterType.from_kind(parameter.kind),
        )


@dataclass(frozen=True)
class Resolvable(Generic[S]):
    parameter: Parameter
    specification: S
    argument: Union[Any, MissingType] = Missing

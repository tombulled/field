import inspect
from dataclasses import dataclass
from typing import Any, Generic, Sequence, TypeVar

from arguments import Arguments, BoundArguments

from .enums import ParameterType
from .sentinels import Missing
from .typing import AnyCallable, AnyOrMissing, Argument
from .utils import parse_parameter_value

__all__: Sequence[str] = (
    # arguments
    "Arguments",
    "BoundArguments",
    # param
    "Parameter",
    "Resolvable",
    "ResolutionContext",
)

M = TypeVar("M")


@dataclass(frozen=True)
class Parameter:
    name: str
    default: AnyOrMissing = Missing
    annotation: AnyOrMissing = Missing
    type: ParameterType = ParameterType.POSITIONAL_OR_KEYWORD

    @classmethod
    def from_parameter(cls, parameter: inspect.Parameter, /) -> "Parameter":
        return cls(
            name=parameter.name,
            default=parse_parameter_value(parameter.default),
            annotation=parse_parameter_value(parameter.annotation),
            type=ParameterType(parameter.kind),
        )


@dataclass(frozen=True)
class Resolvable:
    parameter: Parameter
    metadata: Sequence[Any]
    argument: Argument = Missing


@dataclass(frozen=True)
class ResolutionContext(Generic[M]):
    callable: AnyCallable
    parameter: Parameter
    metadata: M

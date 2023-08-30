import inspect
from dataclasses import dataclass
from typing import Any, Generic, Sequence, TypeVar

from arguments import Arguments, BoundArguments

from .enums import ParameterType
from .parameters import Param
from .sentinels import Undefined
from .utils import parse

__all__: Sequence[str] = (
    # arguments
    "Arguments",
    "BoundArguments",
    # param
    "Parameter",
    "Resolvable",
)

T = TypeVar("T")
P = TypeVar("P", bound=Param)


@dataclass(frozen=True)
class Parameter:
    name: str
    default: Any = Undefined
    annotation: Any = Undefined
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
class Resolvable(Generic[P]):
    parameter: Parameter
    field: P
    argument: Any = Undefined

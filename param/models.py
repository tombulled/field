import inspect
from dataclasses import dataclass
from typing import Any, Generic, Sequence, TypeVar, Union

from arguments import Arguments, BoundArguments

from .enums import ParameterType
from .parameters import Param
from .sentinels import Undefined, UndefinedType
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
    default: Union[Any, UndefinedType] = Undefined
    annotation: Union[Any, UndefinedType] = Undefined
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
    argument: Union[Any, UndefinedType] = Undefined

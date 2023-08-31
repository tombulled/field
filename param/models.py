import inspect
from dataclasses import dataclass
from typing import Any, Generic, Sequence, TypeVar, Union

from arguments import Arguments, BoundArguments
from pydantic.fields import FieldInfo

from .enums import ParameterType
from .sentinels import Undefined, UndefinedType
from .utils import parse_parameter_value

__all__: Sequence[str] = (
    # arguments
    "Arguments",
    "BoundArguments",
    # param
    "Parameter",
    "Resolvable",
)

T = TypeVar("T")
F = TypeVar("F", bound=FieldInfo)


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
            default=parse_parameter_value(parameter.default),
            annotation=parse_parameter_value(parameter.annotation),
            type=ParameterType(parameter.kind),
        )


@dataclass(frozen=True)
class Resolvable(Generic[F]):
    parameter: Parameter
    field: F
    argument: Union[Any, UndefinedType] = Undefined

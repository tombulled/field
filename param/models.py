import inspect
from dataclasses import dataclass
from typing import Any, Generic, Sequence, TypeVar

from arguments import Arguments, BoundArguments

from .enums import ParameterType
from .sentinels import Missing
from .typing import AnyOrMissing
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
    annotation: AnyOrMissing = Missing
    default: AnyOrMissing = Missing
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
    argument: AnyOrMissing = Missing


@dataclass(frozen=True)
class ResolutionContext(Generic[M]):
    # NOTE: Here last.
    # Surely it's only really Pydantic that has a reasonable need to inspect
    # the parameter `name` and `annotation`, and these can be stored in `FieldInfo`
    # by doing a first "sweep" of the params (name -> alias, annotation -> annotation)
    # Provided this is the case, a resolver should just be (metadata: M, argument: Any) -> Any
    name: str
    annotation: Any
    metadata: M

import inspect
from dataclasses import dataclass
from typing import Sequence, TypeVar

from arguments import Arguments, BoundArguments

from .enums import ParameterType
from .sentinels import Missing
from .typing import AnyOrMissing
from .utils import empty_to_missing

__all__: Sequence[str] = (
    # arguments
    "Arguments",
    "BoundArguments",
    # param
    "Parameter",
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
            default=empty_to_missing(parameter.default),
            annotation=empty_to_missing(parameter.annotation),
            type=ParameterType(parameter.kind),
        )

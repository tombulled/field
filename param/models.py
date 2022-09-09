from dataclasses import dataclass, field
from typing import Any, Dict, Generic, Tuple, TypeVar, Union

from .enums import ParameterType
from .sentinels import Missing, MissingType
from .parameters import ParameterSpecification

PT = TypeVar("PT", bound=ParameterSpecification)


@dataclass(frozen=True)
class Arguments:
    args: Tuple[Any, ...] = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    arguments: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Parameter(Generic[PT]):
    name: str
    spec: PT
    type: ParameterType = ParameterType.POSITIONAL_OR_KEYWORD
    annotation: Union[Any, MissingType] = Missing

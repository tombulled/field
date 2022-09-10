from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Generic, Tuple, TypeVar, Union

from .enums import ParameterType
from .parameters import ParameterSpecification
from .sentinels import Missing, MissingType

T = TypeVar("T")
PT = TypeVar("PT", bound=ParameterSpecification)


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
class Parameter(Generic[PT]):
    name: str
    spec: PT
    type: ParameterType = ParameterType.POSITIONAL_OR_KEYWORD
    annotation: Union[Any, MissingType] = Missing

from typing import Any, Callable, Sequence, TypeVar, Union

from typing_extensions import TypeAlias

from .sentinels import MissingType

__all__: Sequence[str] = (
    "AnyCallable",
    "Maybe",
    "AnyOrMissing",
    "Argument",
)

T = TypeVar("T")

AnyCallable = Callable[..., Any]

Maybe = Union[T, MissingType]

AnyOrMissing = Maybe[Any]

Argument: TypeAlias = AnyOrMissing

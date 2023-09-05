from typing import Any, Callable, Sequence, TypeVar, Union

from .sentinels import MissingType

__all__: Sequence[str] = (
    "AnyCallable",
    "Maybe",
    "AnyOrMissing",
)

T = TypeVar("T")

Maybe = Union[T, MissingType]
AnyCallable = Callable[..., Any]
AnyOrMissing = Maybe[Any]

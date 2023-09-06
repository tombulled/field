from typing import Any, Callable, Sequence, TypeVar, Union

from .sentinels import MissingType

__all__: Sequence[str] = (
    "AnyCallable",
    "AnyOrMissing",
)

T = TypeVar("T")

OrMissing = Union[T, MissingType]

AnyCallable = Callable[..., Any]
AnyOrMissing = OrMissing[Any]

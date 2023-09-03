from typing import Any, Callable, Literal, Sequence, TypeVar, Union

from .sentinels import MissingType

__all__: Sequence[str] = (
    "AnyCallable",
    # "AnyOrUndefined",
    "Maybe",
)

T = TypeVar("T")

AnyCallable = Callable[..., Any]
# AnyOrUndefined = Union[Any, UndefinedType]

Maybe = Union[T, MissingType]

from typing import Any, Callable, Sequence, Union

from .sentinels import UndefinedType

__all__: Sequence[str] = (
    "AnyCallable",
    "AnyOrUndefined",
)

AnyCallable = Callable[..., Any]
AnyOrUndefined = Union[Any, UndefinedType]

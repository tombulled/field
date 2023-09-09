from typing import Any, Callable, Sequence, TypeVar

__all__: Sequence[str] = ("AnyCallable",)

T = TypeVar("T")

AnyCallable = Callable[..., Any]

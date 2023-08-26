from typing import Any, Callable, Protocol, Sequence, TypeVar

__all__: Sequence[str] = ("AnyCallable", "Supplier", "Consumer", "Function")

T_contra = TypeVar("T_contra", contravariant=True)
T_co = TypeVar("T_co", covariant=True)
R_co = TypeVar("R_co", covariant=True)

AnyCallable = Callable[..., Any]


class Supplier(Protocol[T_co]):
    def __call__(self) -> T_co:
        ...


class Consumer(Protocol[T_contra]):
    def __call__(self, value: T_contra, /) -> None:
        ...


class Function(Protocol[T_contra, R_co]):
    def __call__(self, value: T_contra, /) -> R_co:
        ...

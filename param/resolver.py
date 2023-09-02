from typing import Protocol, Sequence, TypeVar, runtime_checkable

from .typing import Argument

__all__: Sequence[str] = ("Resolver",)

R_co = TypeVar("R_co", covariant=True)
M_cont = TypeVar("M_cont", contravariant=True)


@runtime_checkable
class Resolver(Protocol[M_cont, R_co]):
    def __call__(self, metadata: M_cont, argument: Argument) -> R_co:
        ...

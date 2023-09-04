from typing import Protocol, Sequence, TypeVar, runtime_checkable

from .models import ResolutionContext
from .typing import Argument

__all__: Sequence[str] = ("Resolver",)

M = TypeVar("M")
R_co = TypeVar("R_co", covariant=True)


@runtime_checkable
class Resolver(Protocol[M, R_co]):
    def __call__(self, context: ResolutionContext[M], argument: Argument) -> R_co:
        ...

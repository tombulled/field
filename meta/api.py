from abc import abstractmethod
from typing import Any, Protocol, TypeVar, runtime_checkable

__all__ = ("Resolver",)

M_contra = TypeVar("M_contra", contravariant=True)
R_co = TypeVar("R_co", covariant=True)


@runtime_checkable
class Resolver(Protocol[M_contra, R_co]):
    @abstractmethod
    def __call__(self, metadata: M_contra, value: Any, /) -> R_co:
        raise NotImplementedError

from abc import abstractmethod
from typing import (
    Any,
    Callable,
    Mapping,
    MutableMapping,
    Protocol,
    Sequence,
    Type,
    TypeVar,
    runtime_checkable,
)

from typing_extensions import TypeAlias

__all__: Sequence[str] = ("Resolver", "Resolvers", "MutableResolvers")

M = TypeVar("M")
R = TypeVar("R")

M_contra = TypeVar("M_contra", contravariant=True)
R_co = TypeVar("R_co", covariant=True)


@runtime_checkable
class Resolver(Protocol[M_contra, R_co]):
    @abstractmethod
    def __call__(self, metadata: M_contra, value: Any, /) -> R_co:
        ...


Resolvers: TypeAlias = Mapping[Type[M], Resolver[M, R]]
MutableResolvers: TypeAlias = MutableMapping[Type[M], Resolver[M, R]]

class ResolversMap(dict, MutableResolvers[M, R]):
    def __call__(
        self, metadata_cls: Type[M], /
    ) -> Callable[[Resolver[M, R]], Resolver[M, R]]:
        def wrapper(resolver: Resolver[M, R], /) -> Resolver[M, R]:
            self[metadata_cls] = resolver

            return resolver

        return wrapper

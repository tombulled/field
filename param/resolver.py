from typing import (
    Any,
    Mapping,
    MutableMapping,
    Protocol,
    Sequence,
    TypeVar,
    runtime_checkable,
)

from typing_extensions import TypeAlias

__all__: Sequence[str] = ("Resolver", "Resolvers", "MutableResolvers")

M_contra = TypeVar("M_contra", contravariant=True)
R_co = TypeVar("R_co", covariant=True)


@runtime_checkable
class Resolver(Protocol[M_contra, R_co]):
    def __call__(self, metadata: M_contra, argument: Any, /) -> R_co:
        ...


Resolvers: TypeAlias = Mapping[type, Resolver]
MutableResolvers: TypeAlias = MutableMapping[type, Resolver]

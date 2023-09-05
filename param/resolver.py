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

from .models import ResolutionContext

__all__: Sequence[str] = ("Resolver", "Resolvers", "MutableResolvers")

M = TypeVar("M")
R_co = TypeVar("R_co", covariant=True)


@runtime_checkable
class Resolver(Protocol[M, R_co]):
    def __call__(self, context: ResolutionContext[M], argument: Any, /) -> R_co:
        ...


Resolvers: TypeAlias = Mapping[type, Resolver]
MutableResolvers: TypeAlias = MutableMapping[type, Resolver]

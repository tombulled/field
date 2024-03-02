from abc import abstractmethod
from typing import Any, Optional, Protocol, TypeVar, runtime_checkable

from meta.errors import ResolutionError

M = TypeVar("M")
R = TypeVar("R")

M_contra = TypeVar("M_contra", contravariant=True)
R_co = TypeVar("R_co", covariant=True)


# Think of this a bit like a redux reducer
@runtime_checkable
class Resolver(Protocol[M_contra, R_co]):
    @abstractmethod
    def __call__(self, metadata: M_contra, value: Any, /) -> R_co:
        raise NotImplementedError


# Note: rename to ResolverGroup?
# class MetadataManager:
# add(key, resolver)
# remove(key)
# get


class ResolverGroup(Resolver[M, R]):
    def __call__(self, metadata: M, value: Any) -> R:
        return self.resolve(metadata, value)

    @abstractmethod
    def get_resolver(self, metadata: M, /) -> Optional[Resolver[M, R]]:
        raise NotImplementedError

    def can_resolve(self, metadata: M, /) -> bool:
        return self.get_resolver(metadata) is not None
    
    def resolve(self, metadata: M, value: Any) -> R:
        resolver: Optional[Resolver[M, R]] = self.get_resolver(metadata)

        if resolver is None:
            raise ResolutionError(
                f"No resolver available for metadata {metadata!r}"
            )

        try:
            return resolver(metadata, value)
        except Exception as error:
            raise ResolutionError(
                f"Failed to resolve value {value!r} through resolver {resolver!r}"
            ) from error
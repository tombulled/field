from abc import abstractmethod
from typing import Any, Dict, Mapping, Optional, Type, TypeVar

from meta.api import Resolver
from meta.errors import ResolutionError

K = TypeVar("K")
M = TypeVar("M")
R = TypeVar("R")


class BaseResolverGroup(Mapping[K, Resolver[M, R]], Resolver[M, R]):
    # def __repr__(self) -> str:
    #     return f"{type(self).__name__}({super().__repr__()})"
    
    def __call__(self, metadata: M, value: Any) -> R:
        return self.resolve(metadata, value)

    def resolve(self, metadata: M, value: Any) -> R:
        resolver: Optional[Resolver[M, R]] = self.get_resolver(metadata)

        if resolver is None:
            raise ResolutionError(f"No resolver available for metadata {metadata!r}")

        try:
            return resolver(metadata, value)
        except Exception as error:
            raise ResolutionError(
                f"Failed to resolve value {value!r} through resolver {resolver!r}"
            ) from error

    @abstractmethod
    def get_resolver(self, metadata: M, /) -> Optional[Resolver[M, R]]:
        raise NotImplementedError

    def can_resolve(self, metadata: M, /) -> bool:
        return self.get_resolver(metadata) is not None


class LiteralResolverGroupABC(BaseResolverGroup[M, M, R]):
    def get_resolver(self, metadata: M, /) -> Optional[Resolver[M, R]]:
        return self.get(metadata)


class LiteralResolverGroup(Dict[M, Resolver[M, R]], LiteralResolverGroupABC[M, R]):
    pass


class ResolverGroupABC(BaseResolverGroup[Type[M], M, R]):
    def get_resolver(self, metadata: M, /) -> Optional[Resolver[M, R]]:
        typ: type
        for typ in type(metadata).mro():
            if typ in self:
                return self[typ]

        return None


class ResolverGroup(Dict[Type[M], Resolver[M, R]], ResolverGroupABC[M, R]):
    pass

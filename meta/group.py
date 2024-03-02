from typing import Any, Dict, Mapping, Optional, Type, TypeVar

from meta.api import Resolver
from meta.errors import ResolutionError

M = TypeVar("M")
R = TypeVar("R")


class LiteralResolverGroupABC(Mapping[M, Resolver[M, R]], Resolver[M, R]):
    def __call__(self, metadata: M, value: Any) -> R:
        resolver: Optional[Resolver[M, R]] = self.get(metadata)

        if resolver is None:
            raise ResolutionError

        return resolver(metadata, value)


class LiteralResolverGroup(Dict[M, Resolver[M, R]], LiteralResolverGroupABC[M, R]):
    pass


class ResolverGroupABC(Mapping[Type[M], Resolver[M, R]], Resolver[M, R]):
    def __call__(self, metadata: M, value: Any) -> R:
        resolver: Optional[Resolver[M, R]] = self._get_resolver(metadata)

        if resolver is None:
            raise ResolutionError

        return resolver(metadata, value)

    def _get_resolver(self, metadata: M, /) -> Optional[Resolver[M, R]]:
        for cls in type(metadata).mro():
            if cls in self:
                return self[cls]

        return None


class ResolverGroup(Dict[Type[M], Resolver[M, R]], ResolverGroupABC[M, R]):
    pass

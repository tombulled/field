from typing import Any, Callable, Dict, Mapping, MutableMapping, Optional, Type, TypeVar
from typing_extensions import TypeAlias

from meta.errors import ResolutionError
from meta.api import Resolver

M = TypeVar("M")
R = TypeVar("R")

Resolvers: TypeAlias = Mapping[Type[M], Resolver[M, R]]
MutableResolvers: TypeAlias = MutableMapping[Type[M], Resolver[M, R]]


class Meta(Dict[Type[M], Resolver[M, R]], MutableResolvers[M, R]):
    def __repr__(self) -> str:
        return f"{type(self).__name__}({super().__repr__()})"

    def get_resolver(self, metadata_cls: Type[M], /) -> Optional[Resolver[M, R]]:
        most_accurate_resolver: Optional[Resolver[M, R]] = None
        min_mro_index: Optional[int] = None

        resolver_metadata_cls: Type[M]
        resolver: Resolver[M, R]
        for resolver_metadata_cls, resolver in self.items():
            # If the resolver isn't a match, skip.
            if not issubclass(metadata_cls, resolver_metadata_cls):
                continue

            mro_index: int = metadata_cls.mro().index(metadata_cls)

            # If this is the new "most accurate" resolver
            if min_mro_index is None or mro_index < min_mro_index:
                most_accurate_resolver = resolver

        return most_accurate_resolver

    def can_resolve(self, metadata_cls: Type[M], /) -> bool:
        return self.get_resolver(metadata_cls) is not None

    def resolve(self, metadata: M, value: Any) -> R:
        """
        >>> meta.resolve(Punctuate("?"), "hello")
        "hello?"
        """
        resolved_value: R = value

        resolver: Optional[Resolver[M, R]] = self.get_resolver(type(metadata))

        if resolver is None:
            raise ResolutionError(
                f"No resolver available for metadata of type {type(metadata)!r}"
            )

        try:
            return resolver(metadata, resolved_value)
        except Exception as error:
            raise ResolutionError(
                f"Failed to resolve value {value!r} through resolver {resolver!r}"
            ) from error

    def resolver(
        self, metadata_cls: Type[M], /
    ) -> Callable[[Resolver[M, R]], Resolver[M, R]]:
        def wrapper(resolver: Resolver[M, R], /) -> Resolver[M, R]:
            self[metadata_cls] = resolver

            return resolver

        return wrapper

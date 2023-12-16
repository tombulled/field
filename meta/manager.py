from typing import Any, Callable, Optional, Sequence, Type, TypeVar

from .api import MetadataManager
from .at import utils
from .errors import ResolutionError
from .resolver import Resolver, Resolvers

M = TypeVar("M")
R = TypeVar("R")


class Meta(MetadataManager[M, R]):
    def __init__(
        self,
        resolvers: Optional[Resolvers[M, R]] = None,
        /,
    ) -> None:
        self.resolvers = {**resolvers} if resolvers is not None else {}

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.resolvers!r})"

    def resolver(
        self, metadata_cls: Type[M], /
    ) -> Callable[[Resolver[M, R]], Resolver[M, R]]:
        def wrapper(resolver: Resolver[M, R], /) -> Resolver[M, R]:
            self.resolvers[metadata_cls] = resolver

            return resolver

        return wrapper

    def get_resolver(self, metadata_cls: Type[M], /) -> Optional[Resolver[M, R]]:
        resolver_metadata_cls: Type[M]
        resolver: Resolver[M, R]
        for resolver_metadata_cls, resolver in self.resolvers.items():
            # WARN: Resolvers should instead be scored/ranked,
            # e.g. a DogResolver should take precedence over an AnimalResolver
            if issubclass(metadata_cls, resolver_metadata_cls):
                return resolver

        return None

    # Current problem: this implementation makes perfect sense
    # for parsing metadata (e.g. Prefix("foo"), Suffix("bar")).
    # However, it makes no sense for validation metadata,
    # (e.g. Gt(10), Len(5))).
    # The MetadataManager class feels like it should perhaps be made
    # bespokely for the metadata it manages, or a few size-fits-all
    # classes could be provided.
    # "resolution strategy"?
    # I think this method should go back to supporting
    # resolving just one piece of metadata? (or also implement a resolve_all?)
    def resolve(self, value: Any, *metadatas: M) -> R:
        resolved_value: R = value

        metadata: M
        for metadata in metadatas:
            resolver: Optional[Resolver[M, R]] = self.get_resolver(type(metadata))

            if resolver is None:
                raise ResolutionError(
                    f"No resolver available for metadata of type {type(metadata)!r}"
                )

            # try:
            resolved_value = resolver(metadata, resolved_value)
            # except Exception as error:
            #     raise ResolutionError(
            #         f"Failed to resolve value {value!r} through resolver {resolver!r}"
            #     ) from error

        return resolved_value

    def parse(self, annotation: Any, /) -> Sequence[M]:
        return [
            metadata
            for metadata in utils.get_metadata(annotation)
            if self.can_resolve(type(metadata))
        ]

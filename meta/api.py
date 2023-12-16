from abc import abstractmethod
from inspect import Parameter
from typing import Any, Callable, Optional, Protocol, Sequence, Type, TypeVar

from typing_extensions import ParamSpec

from .errors import ResolutionError
from .resolver import MutableResolvers, Resolver, Resolvers

M_contra = TypeVar("M_contra", contravariant=True)
R_co = TypeVar("R_co", covariant=True)

M = TypeVar("M", contravariant=True)
R = TypeVar("R", covariant=True)

PS = ParamSpec("PS")
RT = TypeVar("RT")


class ResolverGroup(Resolver[M, R]):
    resolvers: Resolvers[M, R]

    def __call__(self, meta: M, value: Any, /) -> R:
        raise NotImplementedError


# class MetadataManager(Protocol[M, R]):
class MetadataManager(Resolver[M, R]):
    # resolvers: MutableResolvers[M, R]
    resolvers: Resolvers[M, R]

    def __call__(self, metadata: M, value: Any) -> R:
        return self.resolve(metadata, value)

    # @abstractmethod
    # def resolve(self, value: Any, *metadatas: M) -> R:
    # def resolve(self, value: Any, metadata: M) -> R:
    def resolve(self, metadata: M, value: Any) -> R:
        """
        >>> meta.resolve("hello", Punctuate("!!!"))
        "hello!!!"
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

    # This assumes the MetadataManager is *mutable*, which it may not be.
    # @abstractmethod
    # def resolver(
    #     self, metadata_cls: Type[M], /
    # ) -> Callable[[Resolver[M, R]], Resolver[M, R]]:
    #     """
    #     @meta.resolver(Suffix)
    #     def suffix(metadata: Suffix, argument: Any) -> str:
    #         assert isinstance(argument, str)

    #         return argument + metadata.suffix
    #     """
    #     ...

    # What if the metadata manager isn't in the mood for sharing?
    # @abstractmethod
    def get_resolver(self, metadata_cls: Type[M], /) -> Optional[Resolver[M, R]]:
        """
        >>> meta.get_resolver(Dog)
        <function resolve_animal at 0x7f057a88a4c0>
        """
        # raise NotImplementedError

        resolver_metadata_cls: Type[M]
        resolver: Resolver[M, R]
        for resolver_metadata_cls, resolver in self.resolvers.items():
            # WARN: Resolvers should instead be scored/ranked,
            # e.g. a DogResolver should take precedence over an AnimalResolver
            if issubclass(metadata_cls, resolver_metadata_cls):
                return resolver

        return None

    def can_resolve(self, metadata_cls: Type[M], /) -> bool:
        """
        >>> meta.can_resolve(Dog)
        True
        """
        return self.get_resolver(metadata_cls) is not None

    # @abstractmethod
    # def parse(self, annotation: Any, /) -> Sequence[M]:
    #     """
    #     meta = MetadataManager({Punctuate: resolve_punctuate})

    #     >>> meta.parse(Annotated[str, Punctuate("!")])
    #     [Punctuate("!")]
    #     """
    #     ...


class ParameterMetadataManager(Protocol[M, R]):
    metadata_manager: MetadataManager[M, R]

    @abstractmethod
    def wrap(self, func: Callable[PS, RT], /) -> Callable[PS, RT]:
        """
        @params.wrap
        def greet(name: Name) -> str:
            return f"Hello, {name}!"

        >>> greet("bob dylan")
        Hello, Bob Dylan!
        """
        ...

    @abstractmethod
    def resolve(
        self, func: Callable[..., RT], arguments
    ) -> RT:  # TODO: Type `arguments`
        """
        def greet(name: Name) -> str:
            return f"Hello, {name}!"

        >>> resolve(greet, Arguments("bob dylan"))
        Hello, Bob Dylan!
        """
        ...

    @abstractmethod
    def resolve_parameter(self, parameter: Parameter, argument: Any) -> R:
        """
        >>> params.resolve_parameter(name_parameter, "bob dylan")
        "Bob Dylan"
        """
        ...

from abc import abstractmethod
from typing import Any, Callable, Optional, Protocol, Sequence, Type, TypeVar

from typing_extensions import ParamSpec

from . import utils
from .resolver import MutableResolvers, Resolver

M = TypeVar("M")
R = TypeVar("R")

PS = ParamSpec("PS")
RT = TypeVar("RT")


class MetadataManager(Protocol[M, R]):
    resolvers: MutableResolvers[M, R]

    @abstractmethod
    def resolver(
        self, metadata_cls: Type[M], /
    ) -> Callable[[Resolver[M, R]], Resolver[M, R]]:
        """
        @meta.resolver(Suffix)
        def suffix(metadata: Suffix, argument: Any) -> str:
            assert isinstance(argument, str)

            return argument + metadata.suffix
        """
        ...

    @abstractmethod
    def get_resolver(self, metadata_cls: Type[M], /) -> Optional[Resolver[M, R]]:
        """
        >>> meta.get_metadata(Dog)
        <function resolve_animal at 0x7f057a88a4c0>
        """
        ...

    @abstractmethod
    def can_resolve(self, metadata_cls: Type[M], /) -> bool:
        """
        >>> meta.can_resolve(Dog)
        True
        """
        ...

    @abstractmethod
    def resolve(self, value: Any, *metadatas: M) -> R:
        """
        >>> meta.resolve("hello", Punctuate("!!!"))
        "hello!!!"
        """
        ...

    @abstractmethod
    def extract(self, annotation: Any, /) -> Sequence[M]:
        """
        meta = MetadataManager({Punctuate: resolve_punctuate})

        >>> meta.extract(Annotated[str, Punctuate("!")])
        [Punctuate("!")]
        """
        ...


class ParameterMetadataManager(Protocol):
    def __call__(self, func: Callable[PS, RT], /) -> Callable[PS, RT]:
        """
        @params
        def greet(name: Name) -> str:
            return f"Hello, {name}!"

        >>> greet("bob dylan")
        Hello, Bob Dylan!
        """
        ...

    def resolve(self, func, arguments):
        """
        def greet(name: Name) -> str:
            return f"Hello, {name}!"

        >>> resolve(greet, Arguments("bob dylan"))
        Hello, Bob Dylan!
        """
        ...

    def resolve_parameter(self, parameter, argument):
        """
        >>> params.resolve_parameter(name_parameter, "bob dylan")
        "Bob Dylan"
        """
        ...

    # get_metadata
    # get_parameter_metadata

import functools
import inspect
from typing import (
    Any,
    Callable,
    Generic,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
)

from arguments import Arguments, BoundArguments
from typing_extensions import ParamSpec

from . import utils
from .errors import ResolutionError
from .resolver import MutableResolvers, Resolver, Resolvers

__all__: Sequence[str] = ("Params",)

M = TypeVar("M")
R = TypeVar("R")

PS = ParamSpec("PS")
RT = TypeVar("RT")


class Params(Generic[M, R]):
    # TODO: Configure what to do if unsupported metadata found (e.g. ignore vs throw)
    
    resolvers: MutableResolvers[M, R]

    def __init__(
        self,
        resolvers: Optional[Resolvers[M, R]] = None,
        /,
    ) -> None:
        self.resolvers = {**resolvers} if resolvers is not None else {}

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.resolvers!r})"

    def __call__(self, func: Callable[PS, RT], /) -> Callable[PS, RT]:
        @functools.wraps(func)
        def wrapper(*args: PS.args, **kwargs: PS.kwargs) -> RT:
            arguments: Arguments = Arguments(*args, **kwargs)

            resolved_arguments: Arguments = self.resolve(func, arguments)

            bound_arguments: BoundArguments = resolved_arguments.bind(func)

            return bound_arguments.call(func)

        return wrapper

    def resolver(
        self, metadata_cls: Type[M], /
    ) -> Callable[[Resolver[M, R]], Resolver[M, R]]:
        def wrapper(resolver: Resolver[M, R], /) -> Resolver[M, R]:
            self.resolvers[metadata_cls] = resolver

            return resolver

        return wrapper

    def get_resolver(self, metadata: M, /) -> Optional[Resolver[M, R]]:
        metadata_cls: Type[M] = type(metadata)

        # NOTE: For now this is naive, however, in the future, may want
        # to do a subclass check (e.g. Dog would match a resolver for Animal)
        return self.resolvers.get(metadata_cls)

    def can_resolve(self, metadata: M, /) -> bool:
        return self.get_resolver(metadata) is not None

    def resolve_metadata(self, metadata: M, argument: Any) -> R:
        resolver: Optional[Resolver[M, R]] = self.get_resolver(metadata)

        if resolver is None:
            raise ResolutionError(
                f"No resolver available for metadata of type {type(metadata)!r}"
            )

        return resolver(metadata, argument)

    def get_metadata(self, typ: Any, /) -> Sequence[M]:
        return [
            metadata
            for metadata in utils.get_metadata(typ)
            if self.can_resolve(metadata)
        ]

    def get_parameter_metadata(self, parameter: inspect.Parameter, /) -> Sequence[M]:
        return self.get_metadata(parameter.annotation)

    def resolve(self, func: Callable[..., Any], arguments: Arguments) -> Arguments:
        bound_arguments: BoundArguments = arguments.bind(func)

        parameters: Mapping[str, inspect.Parameter] = inspect.signature(func).parameters

        args: MutableMapping[str, Any] = {}
        kwargs: MutableMapping[str, Any] = {}

        parameter: inspect.Parameter
        for parameter in parameters.values():
            argument: Any = bound_arguments.get(parameter.name)
            metadatas: Sequence[Any] = self.get_parameter_metadata(parameter)

            metadata: Any
            for metadata in metadatas:
                argument = self.resolve_metadata(metadata, argument)

            if parameter.name in bound_arguments.kwargs:
                kwargs[parameter.name] = argument
            else:
                args[parameter.name] = argument

        return Arguments(*args.values(), **kwargs)

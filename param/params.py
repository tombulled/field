import functools
from typing import (
    Any,
    Callable,
    Iterable,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
)

from arguments import Arguments, BoundArguments
from typing_extensions import ParamSpec, TypeAlias

from . import api, utils
from .errors import ResolutionError
from .models import Parameter, Resolvable, ResolutionContext
from .resolver import Resolver
from .typing import AnyCallable

__all__: Sequence[str] = ("Params",)

M = TypeVar("M")
R = TypeVar("R")

PS = ParamSpec("PS")
RT = TypeVar("RT")

Resolvers: TypeAlias = Mapping[type, Resolver]
MutableResolvers: TypeAlias = MutableMapping[type, Resolver]


class Params:
    resolvers: MutableResolvers

    def __init__(
        self,
        resolvers: Optional[Resolvers] = None,
        /,
    ) -> None:
        self.resolvers = {**resolvers} if resolvers is not None else {}

    def __call__(self, func: Callable[PS, RT], /) -> Callable[PS, RT]:
        @functools.wraps(func)
        def wrapper(*args: PS.args, **kwargs: PS.kwargs) -> RT:
            arguments: Arguments = Arguments(*args, **kwargs)

            bound_arguments: BoundArguments = self.get_arguments(func, arguments)

            return bound_arguments.call(func)

        return wrapper

    def _get_resolvables(
        self, func: AnyCallable, arguments: Arguments, /
    ) -> Mapping[str, Resolvable]:
        bound_arguments: BoundArguments = arguments.bind(func)
        parameters: Mapping[str, Parameter] = api.get_parameters(func)
        resolvables: MutableMapping[str, Resolvable] = {}

        parameter_name: str
        argument: Any
        for parameter_name, argument in bound_arguments.asdict().items():
            parameter: Parameter = parameters[parameter_name]

            metadata: Sequence[Any] = self.get_metadata(parameter)

            resolvable: Resolvable = Resolvable(
                parameter=parameter,
                metadata=metadata,
                argument=argument,
            )

            resolvables[parameter_name] = resolvable

        return resolvables

    def get_metadata(self, parameter: Parameter, /) -> Sequence[Any]:
        return [
            metadata
            for metadata in utils.get_metadata(parameter.annotation)
            if self.has_resolver(type(metadata))
        ]

    def has_resolver(self, metadata_cls: type, /) -> bool:
        # NOTE: For now this is naive, however in the future may want
        # to do subclass checks (e.g. Dog would match a resolver for Animal)
        return metadata_cls in self.resolvers

    def get_resolver(self, metadata_cls: Type[M], /) -> Resolver[M, Any]:
        if not self.has_resolver(metadata_cls):
            raise ResolutionError(f"No resolver for metadata {metadata_cls}")

        # NOTE: For now this is naive, however in the future may want
        # to do subclass checks (e.g. Dog would match a resolver for Animal)
        return self.resolvers[metadata_cls]

    def resolve(
        self,
        func: AnyCallable,
        resolvable: Resolvable,
    ) -> Any:
        argument: Any = resolvable.argument

        metadata: Any
        for metadata in resolvable.metadata:
            metadata_cls: type = type(metadata)
            resolver: Resolver = self.get_resolver(metadata_cls)

            resolution_context: ResolutionContext[Any] = ResolutionContext(
                callable=func,
                parameter=resolvable.parameter,
                metadata=metadata,
            )

            argument = resolver(resolution_context, argument)

        return argument

    def resolve_all(
        self,
        func: AnyCallable,
        resolvables: Iterable[Resolvable],
        /,
    ) -> Mapping[str, Any]:
        return {
            resolvable.parameter.name: self.resolve(func, resolvable)
            for resolvable in resolvables
        }

    def resolver(self, metadata_cls: Type[M], /):  # TODO: Type me
        def wrapper(resolver: Resolver[M, R], /) -> Resolver[M, R]:
            self.resolvers[metadata_cls] = resolver

            return resolver

        return wrapper

    def get_arguments(self, func: AnyCallable, arguments: Arguments) -> BoundArguments:
        resolvables: Mapping[str, Resolvable] = self._get_resolvables(func, arguments)
        parameters: Mapping[str, Parameter] = api.get_parameters(func)
        bound_arguments: BoundArguments = arguments.bind(func)
        resolved_arguments: Mapping[str, Any] = self.resolve_all(func, resolvables.values())

        args: MutableMapping[str, Any] = {}
        kwargs: MutableMapping[str, Any] = {}

        parameter: Parameter
        for parameter in parameters.values():
            destination: MutableMapping[str, Any]

            if parameter.name in bound_arguments.kwargs:
                destination = kwargs
            else:
                destination = args

            argument: Any

            if parameter.name in resolvables:
                argument = resolved_arguments[parameter.name]
            else:
                argument = bound_arguments.get(parameter.name)

            destination[parameter.name] = argument

        return Arguments(*args.values(), **kwargs).bind(func)

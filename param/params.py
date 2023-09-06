import functools
from typing import (
    Any,
    Callable,
    Iterable,
    Mapping,
    MutableMapping,
    Optional,
    Protocol,
    Sequence,
    Type,
    TypeVar,
)

from arguments import Arguments, BoundArguments
from typing_extensions import ParamSpec

from . import api, utils
from .errors import ResolutionError
from .models import Parameter, Resolvable
from .resolver import MutableResolvers, Resolver, Resolvers
from .sentinels import Missing
from .typing import AnyCallable

__all__: Sequence[str] = ("Params",)

M = TypeVar("M")
P = ParamSpec("P")
R = TypeVar("R")

# def get_parameter_annotation(parameter: Parameter, /) -> Any:
#     if parameter.annotation is Missing:
#         return Any

#     if utils.is_annotated(parameter.annotation):
#         return

#     return parameter.annotation


class ResolverIdentityCallable(Protocol[M]):
    def __call__(self, resolver: Resolver[M, R], /) -> Resolver[M, R]:
        ...


class ParamsI(Protocol):
    resolvers: MutableResolvers

    def __call__(self, func: Callable[P, R], /) -> Callable[P, R]:
        """
        params = Params(...)

        @params
        def greet(name: Annotated[str, Uppercase()]):
            ...
        """
        ...

    def get_resolver(self, metadata: M, /) -> Optional[Resolver[M, Any]]:
        ...

    def can_resolve(self, metadata: M, /) -> bool:
        ...

    def resolve_metadata(self, metadata: Any, argument: Any) -> Any:
        ...

    def get_metadata(self, typ: Any, /) -> Sequence[Any]:
        ...

    # def resolve_parameter(self, parameter: Parameter, argument: Any) -> Any:
    #     """
    #     params = Params(...)

    #     parameter = Parameter("name", Annotated[str, Uppercase()])

    #     assert params.resolve_parameter(parameter, "bob") == "BOB"
    #     """
    #     ...

    def resolver(self, metadata_cls: Type[M], /) -> ResolverIdentityCallable[M]:
        """
        params = Params(...)

        @params.resolver(Uppercase)
        def resolve_uppercase(_, argument: Any) -> str:
            ...
        """
        ...

    def resolve(self, func: AnyCallable, arguments: Arguments) -> Arguments:
        """
        params = Params(...)

        def greet(name: Annotated[str, Uppercase()]):
            ...

        assert resolve(greet, Arguments("bob")) == Arguments("BOB")
        """
        ...


class NewParams:
    resolvers: MutableResolvers

    def __init__(
        self,
        resolvers: Optional[Resolvers] = None,
        /,
    ) -> None:
        self.resolvers = {**resolvers} if resolvers is not None else {}

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.resolvers!r})"

    def __call__(self, func: Callable[P, R], /) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            arguments: Arguments = Arguments(*args, **kwargs)

            resolved_arguments: Arguments = self.resolve(func, arguments)

            bound_arguments: BoundArguments = resolved_arguments.bind(func)

            return bound_arguments.call(func)

        return wrapper

    def resolver(self, metadata_cls: Type[M], /) -> ResolverIdentityCallable[M]:
        def wrapper(resolver: Resolver[M, R], /) -> Resolver[M, R]:
            self.resolvers[metadata_cls] = resolver

            return resolver

        return wrapper

    def get_resolver(self, metadata: M, /) -> Optional[Resolver[M, Any]]:
        metadata_cls: Type[M] = type(metadata)

        # NOTE: For now this is naive, however, in the future, may want
        # to do a subclass check (e.g. Dog would match a resolver for Animal)
        return self.resolvers.get(metadata_cls)

    def can_resolve(self, metadata: M, /) -> bool:
        return self.get_resolver(metadata) is not None

    def resolve_metadata(self, metadata: M, argument: Any) -> Any:
        resolver: Optional[Resolver[M, Any]] = self.get_resolver(metadata)

        if resolver is None:
            raise ResolutionError(
                f"No resolver available for metadata of type {type(metadata)!r}"
            )

        return resolver(metadata, argument)

    def get_metadata(self, typ: Any, /) -> Sequence[Any]:
        return [
            metadata
            for metadata in utils.get_metadata(typ)
            if self.can_resolve(metadata)
        ]

    def resolve(self, func: AnyCallable, arguments: Arguments) -> Arguments:
        bound_arguments: BoundArguments = arguments.bind(func)

        args: MutableMapping[str, Any] = {}
        kwargs: MutableMapping[str, Any] = {}

        parameter: Parameter
        for parameter in api.get_parameters(func).values():
            argument: Any = bound_arguments.get(parameter.name)
            metadatas: Sequence[Any] = self.get_metadata(parameter.annotation)

            metadata: Any
            for metadata in metadatas:
                argument = self.resolve_metadata(metadata, argument)

            if parameter.name in bound_arguments.kwargs:
                kwargs[parameter.name] = argument
            else:
                args[parameter.name] = argument

        return Arguments(*args.values(), **kwargs)


class Params:
    resolvers: MutableResolvers

    def __init__(
        self,
        resolvers: Optional[Resolvers] = None,
        /,
    ) -> None:
        self.resolvers = {**resolvers} if resolvers is not None else {}

    def __call__(self, func: Callable[P, R], /) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            arguments: Arguments = Arguments(*args, **kwargs)

            pre_bound_arguments: BoundArguments = arguments.bind(func)

            print(f"Pre BoundArguments: {pre_bound_arguments!r}")

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
            if self.can_resolve(metadata)
        ]

    def has_resolver(self, metadata_cls: type, /) -> bool:
        # NOTE: For now this is naive, however in the future may want
        # to do subclass checks (e.g. Dog would match a resolver for Animal)
        return metadata_cls in self.resolvers

    def can_resolve(self, metadata: Any, /) -> bool:
        # NOTE: For now this is naive, however in the future may want
        # to do subclass checks (e.g. Dog would match a resolver for Animal)
        return type(metadata) in self.resolvers

    def get_resolver(self, metadata_cls: Type[M], /) -> Resolver[M, Any]:
        if not self.has_resolver(metadata_cls):
            raise ResolutionError(f"No resolver for metadata {metadata_cls}")

        # NOTE: For now this is naive, however in the future may want
        # to do subclass checks (e.g. Dog would match a resolver for Animal)
        return self.resolvers[metadata_cls]

    def resolve(
        self,
        resolvable: Resolvable,
    ) -> Any:
        argument: Any = resolvable.argument

        metadata: Any
        for metadata in resolvable.metadata:
            metadata_cls: type = type(metadata)
            resolver: Resolver = self.get_resolver(metadata_cls)

            # TODO: Check if this is Annotated[], and if so, rip out the first arg
            # If is Missing, use Any
            annotation: Any = resolvable.parameter.annotation

            resolution_context: ResolutionContext[Any] = ResolutionContext(
                name=resolvable.parameter.name,
                annotation=annotation,
                metadata=metadata,
            )

            argument = resolver(resolution_context, argument)

        return argument

    def resolve_all(
        self,
        resolvables: Iterable[Resolvable],
        /,
    ) -> Mapping[str, Any]:
        return {
            resolvable.parameter.name: self.resolve(resolvable)
            for resolvable in resolvables
        }

    def resolver(self, metadata_cls: Type[M], /) -> ResolverIdentityCallable[M]:
        def wrapper(resolver: Resolver[M, R], /) -> Resolver[M, R]:
            self.resolvers[metadata_cls] = resolver

            return resolver

        return wrapper

    def get_arguments(self, func: AnyCallable, arguments: Arguments) -> BoundArguments:
        resolvables: Mapping[str, Resolvable] = self._get_resolvables(func, arguments)
        parameters: Mapping[str, Parameter] = api.get_parameters(func)
        bound_arguments: BoundArguments = arguments.bind(func)
        resolved_arguments: Mapping[str, Any] = self.resolve_all(resolvables.values())

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

import dataclasses
import functools
import inspect
from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
)

from typing_extensions import ParamSpec

from .errors import ResolutionError
from .models import Arguments, BoundArguments, Parameter, Resolvable
from .parameters import Param
from .resolvers import RESOLVERS, Resolver, Resolvers
from .sentinels import Undefined
from .typing import AnyCallable

__all__: Sequence[str] = ("ParameterManager", "ParamManager")

PS = ParamSpec("PS")
RT = TypeVar("RT")

R = TypeVar("R", bound=AnyCallable)


@dataclass
class ParameterManager(Generic[R]):
    resolvers: Resolvers[R]

    @staticmethod
    def get_parameters(func: AnyCallable, /) -> Mapping[str, Parameter]:
        return {
            parameter.name: Parameter.from_parameter(parameter)
            for parameter in inspect.signature(func).parameters.values()
        }

    def get_param(self, parameter: Parameter, /) -> Optional[Param]:
        if isinstance(parameter.default, Param):
            return parameter.default
        else:
            return None

    def get_resolver(self, param_cls: Type[Param], /) -> R:
        resolver: Optional[R] = self.resolvers.get(param_cls)

        if resolver is not None:
            return resolver
        else:
            raise ResolutionError(f"No resolver for parameter {param_cls}")

    def resolve(self, resolvable: Resolvable) -> Any:
        raise ResolutionError("Resolution method not implemented")

    def resolve_all(
        self,
        resolvables: Iterable[Resolvable],
        /,
    ) -> Mapping[str, Any]:
        return {
            resolvable.parameter.name: self.resolve(resolvable)
            for resolvable in resolvables
        }

    def get_resolvables(
        self, func: AnyCallable, arguments: Arguments, /
    ) -> Mapping[str, Resolvable]:
        bound_arguments: BoundArguments = arguments.bind(func)
        parameters: Mapping[str, Parameter] = self.get_parameters(func)
        resolvables: MutableMapping[str, Resolvable] = {}

        parameter_name: str
        argument: Any
        for parameter_name, argument in bound_arguments.asdict().items():
            parameter: Parameter = parameters[parameter_name]
            specification: Optional[Param] = self.get_param(parameter)

            if specification is None:
                continue

            if argument is specification:
                argument = Undefined

            resolvable: Resolvable = Resolvable(
                parameter=parameter,
                field=specification,
                argument=argument,
            )

            resolvables[parameter_name] = resolvable

        return resolvables

    def get_arguments(self, func: Callable, arguments: Arguments) -> BoundArguments:
        resolvables: Mapping[str, Resolvable] = self.get_resolvables(func, arguments)
        parameters: Mapping[str, Parameter] = self.get_parameters(func)
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

    def params(self, func: Callable[PS, RT], /) -> Callable[PS, RT]:
        @functools.wraps(func)
        def wrapper(*args: PS.args, **kwargs: PS.kwargs) -> RT:
            arguments: Arguments = Arguments(*args, **kwargs)

            bound_arguments: BoundArguments = self.get_arguments(func, arguments)

            return bound_arguments.call(func)

        return wrapper


@dataclass
class ParamManager(ParameterManager[Resolver]):
    resolvers: Resolvers[Resolver] = field(default_factory=lambda: RESOLVERS)

    def get_param(self, parameter: Parameter, /) -> Param:
        specification: Optional[Param] = super().get_param(parameter)

        if specification is not None:
            return specification
        else:
            return Param(default=parameter.default)

    def resolve(
        self,
        resolvable: Resolvable,
    ) -> Any:
        resolver_cls: Type[Param] = type(resolvable.field)
        resolver: Resolver = self.get_resolver(resolver_cls)

        return resolver(resolvable.field, resolvable.argument)

    def get_resolvables(
        self, func: Callable, arguments: Arguments, /
    ) -> Mapping[str, Resolvable]:
        resolvables: MutableMapping[str, Resolvable] = {}

        parameter_name: str
        resolvable: Resolvable
        for parameter_name, resolvable in (
            super().get_resolvables(func, arguments).items()
        ):
            parameter: Parameter = resolvable.parameter
            field: Param = resolvable.field

            if field.alias is None:
                field = dataclasses.replace(
                    field, alias=field.generate_alias(parameter.name)
                )

                resolvable = dataclasses.replace(resolvable, field=field)

            resolvables[parameter_name] = resolvable

        return resolvables

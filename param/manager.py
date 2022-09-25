import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Generic, Optional, Type, TypeVar, Union

from .enums import ParameterType
from .errors import ResolutionError
from .models import Arguments, BoundArguments, Parameter
from .parameters import Param, ParameterSpecification
from .resolvers import RESOLVERS, Resolver, Resolvers
from .sentinels import Missing, MissingType

R = TypeVar("R", bound=Callable)


def _parse(value: Any, /) -> Union[Any, MissingType]:
    if value is inspect.Parameter.empty:
        return Missing

    return value


def _bind_arguments(func: Callable, arguments: Arguments) -> BoundArguments:
    signature: inspect.Signature = inspect.signature(func)

    bound_arguments: inspect.BoundArguments = arguments.call(signature.bind)

    bound_arguments.apply_defaults()

    bound_args: Dict[str, Any] = dict(zip(signature.parameters, bound_arguments.args))
    bound_kwargs: Dict[str, Any] = bound_arguments.kwargs

    return BoundArguments(args=bound_args, kwargs=bound_kwargs)


@dataclass
class ParameterManager(Generic[R]):
    resolvers: Resolvers[R]

    def get_params(self, func: Callable, /) -> Dict[str, Parameter]:
        params: Dict[str, Parameter] = {}

        parameter: inspect.Parameter
        for parameter in inspect.signature(func).parameters.values():
            default: Union[Any, MissingType] = _parse(parameter.default)

            if not isinstance(default, ParameterSpecification):
                inferred_spec: Optional[ParameterSpecification] = self.infer_spec(
                    parameter
                )

                if inferred_spec is not None:
                    default = inferred_spec

            params[parameter.name] = Parameter(
                name=parameter.name,
                default=default,
                annotation=_parse(parameter.annotation),
                type=ParameterType.from_kind(parameter.kind),
            )

        return params

    def infer_spec(
        self, parameter: inspect.Parameter, /
    ) -> Optional[ParameterSpecification]:
        return None

    def get_resolver(self, param_cls: Type[ParameterSpecification], /) -> R:
        resolver: Optional[R] = self.resolvers.get(param_cls)

        if resolver is not None:
            return resolver
        else:
            raise ResolutionError(f"No resolver for parameter {param_cls}")

    def resolve(
        self,
        parameter: Parameter[ParameterSpecification],
        argument: Union[Any, MissingType],
    ) -> Any:
        raise ResolutionError("Resolution method not implemented")

    def resolve_arguments(
        self,
        arguments: Dict[Parameter[ParameterSpecification], Union[Any, MissingType]],
        /,
    ) -> Dict[str, Any]:
        return {
            parameter.name: self.resolve(parameter, argument)
            for parameter, argument in arguments.items()
        }

    def get_arguments(self, func: Callable, arguments: Arguments) -> BoundArguments:
        bound_arguments: BoundArguments = _bind_arguments(func, arguments)

        parameters: Dict[str, Parameter] = self.get_params(func)

        resolution_arguments: Dict[
            Parameter[ParameterSpecification], Union[Any, MissingType]
        ] = {}

        source: Dict[str, Any]
        for source in (bound_arguments.args, bound_arguments.kwargs):
            parameter_name: str
            argument: Any
            for parameter_name, argument in source.items():
                parameter: Parameter = parameters[parameter_name]

                if not isinstance(parameter.default, ParameterSpecification):
                    continue

                if (
                    isinstance(argument, ParameterSpecification)
                    and argument is parameter.default
                ):
                    argument = Missing

                resolution_arguments[parameter] = argument

        resolved_arguments: Dict[str, Any] = self.resolve_arguments(
            resolution_arguments
        )

        for parameter_name, argument in resolved_arguments.items():
            source = (
                bound_arguments.args
                if parameter_name in bound_arguments.args
                else bound_arguments.kwargs
            )

            source[parameter_name] = argument

        return bound_arguments


@dataclass
class ParamManager(ParameterManager[Resolver]):
    resolvers: Resolvers[Resolver] = field(default_factory=lambda: RESOLVERS)

    def infer_spec(self, parameter: inspect.Parameter, /) -> ParameterSpecification:
        return Param(default=_parse(parameter.default))

    def resolve(
        self,
        parameter: Parameter[ParameterSpecification],
        argument: Union[Any, MissingType],
    ) -> Any:
        return self.get_resolver(type(parameter.default))(parameter, argument)

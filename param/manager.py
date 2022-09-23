import inspect
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Generic, Optional, Type, TypeVar, Union

from .enums import ParameterType
from .errors import MissingSpecification, ResolutionError
from .models import Arguments, BoundArguments, Parameter
from .parameters import Param, ParameterSpecification
from .resolvers import RESOLVERS, Resolver, Resolvers
from .sentinels import Missing, MissingType

R = TypeVar("R", bound=Callable)


def _parse(value: Any, /) -> Union[Any, MissingType]:
    if value is inspect._empty:
        return Missing

    return value


def _bind_arguments(func: Callable[..., Any], arguments: Arguments) -> BoundArguments:
    signature: inspect.Signature = inspect.signature(func)

    bound_arguments: inspect.BoundArguments = arguments.call(signature.bind)

    bound_arguments.apply_defaults()

    bound_args: Dict[str, Any] = dict(zip(signature.parameters, bound_arguments.args))
    bound_kwargs: Dict[str, Any] = bound_arguments.kwargs

    return BoundArguments(args=bound_args, kwargs=bound_kwargs)


class ParameterManager(Generic[R], ABC):
    resolvers: Resolvers[R]
    infer: bool = True

    def get_params(self, func: Callable, /) -> Dict[str, Parameter]:
        params: Dict[str, Parameter] = {}

        parameter: inspect.Parameter
        for parameter in inspect.signature(func).parameters.values():
            spec: ParameterSpecification

            if isinstance(parameter.default, ParameterSpecification):
                spec = parameter.default
            elif self.infer:
                spec = self.infer_parameter(parameter)
            else:
                continue

            param: Parameter = Parameter(
                name=parameter.name,
                annotation=_parse(parameter.annotation),
                type=ParameterType.from_kind(parameter.kind),
                spec=spec,
            )

            params[parameter.name] = param

        return params

    def infer_parameter(
        self, parameter: inspect.Parameter, /
    ) -> ParameterSpecification:
        raise MissingSpecification(f"Missing specification for parameter {parameter}")

    def get_resolver(self, param_cls: Type[ParameterSpecification], /) -> R:
        resolver: Optional[R] = self.resolvers.get(param_cls)

        if resolver is not None:
            return resolver
        else:
            raise ResolutionError(f"No resolver for parameter {param_cls}")

    @abstractmethod
    def resolve(self, parameter: Parameter, argument: Union[Any, MissingType]) -> Any:
        raise NotImplementedError

    def resolve_parameters(
        self,
        parameters: Dict[str, Parameter],
        arguments: Dict[str, Any],
        /,
    ) -> Dict[str, Any]:
        return {
            parameter.name: self.resolve(
                parameter,
                argument if argument is not parameter.spec else Missing,
            )
            for parameter, argument in zip(parameters.values(), arguments.values())
        }

    def get_arguments(self, func: Callable, arguments: Arguments) -> BoundArguments:
        bound_arguments: BoundArguments = _bind_arguments(func, arguments)

        parameters: Dict[str, Parameter] = self.get_params(func)

        resolution_parameters: Dict[str, Parameter] = {}

        source: Dict[str, Any]
        for source in (bound_arguments.args, bound_arguments.kwargs):
            parameter_name: str
            argument: Any
            for parameter_name, argument in source.items():
                if parameter_name not in parameters:
                    continue

                resolution_parameters[parameter_name] = parameters[parameter_name]

        resolution_arguments: Dict[str, Any] = {
            parameter: bound_arguments.arguments[parameter]
            for parameter in resolution_parameters
        }

        resolved_arguments: Dict[str, Any] = self.resolve_parameters(
            resolution_parameters, resolution_arguments
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

    def infer_parameter(
        self, parameter: inspect.Parameter, /
    ) -> ParameterSpecification:
        return Param(default=_parse(parameter.default))

    def resolve(self, parameter: Parameter, argument: Union[Any, MissingType]) -> Any:
        return self.get_resolver(type(parameter.spec))(parameter, argument)

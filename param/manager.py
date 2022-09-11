from abc import ABC, abstractmethod
import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Generic, TypeVar

from .enums import ParameterType
from .errors import MissingSpecification
from .models import Arguments, BoundArguments, Parameter
from .parameters import Param, ParameterSpecification
from .resolvers import Resolvers, resolve_param
from .sentinels import Missing

C = TypeVar("C")


def _parse(value: Any, /) -> Any:
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


class ParameterManager(Generic[C], ABC):
    resolvers: Resolvers[C]
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

    def resolve(self, parameter: Parameter, context: C, argument: Any) -> Any:
        return self.resolvers.resolve(parameter, context, argument)

    @abstractmethod
    def build_contexts(
        self, parameters: Dict[str, Parameter], arguments: Dict[str, Any]
    ) -> Dict[str, C]:
        ...

    def resolve_parameters(
        self,
        parameters: Dict[str, Parameter],
        contexts: Dict[str, C],
        arguments: Dict[str, Any],
        /,
    ) -> Dict[str, Any]:
        return {
            parameter.name: self.resolve(
                parameter,
                context,
                argument if argument is not parameter.spec else Missing,
            )
            for parameter, context, argument in zip(
                parameters.values(), contexts.values(), arguments.values()
            )
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

        resolution_contexts: Dict[str, C] = self.build_contexts(
            resolution_parameters, resolution_arguments
        )

        resolved_arguments: Dict[str, Any] = self.resolve_parameters(
            resolution_parameters, resolution_contexts, resolution_arguments
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
class ParamManager(ParameterManager[None]):
    resolvers: Resolvers[None] = field(
        default_factory=lambda: Resolvers({Param: resolve_param})
    )

    def infer_parameter(
        self, parameter: inspect.Parameter, /
    ) -> ParameterSpecification:
        return Param(default=_parse(parameter.default))

    def build_contexts(
        self, parameters: Dict[str, Parameter], arguments: Dict[str, Any]
    ) -> Dict[str, None]:
        return {parameter: None for parameter in parameters}

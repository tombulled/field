from typing import Any, Protocol, Type, Union

from roster import Register

from .errors import ResolutionError
from .models import Parameter
from .parameters import ParameterSpecification, Param
from .sentinels import Missing, MissingType


class Resolver(Protocol):
    def __call__(
        self, parameter: Parameter, value: Union[Any, MissingType] = Missing, /
    ) -> Any:
        ...


class Resolvers(Register[Type[ParameterSpecification], Resolver]):
    def resolve(
        self, parameter: Parameter, value: Union[Any, MissingType] = Missing, /
    ) -> Any:
        parameter_cls: Type[ParameterSpecification]
        resolver: Resolver
        for parameter_cls, resolver in self.items():
            if type(parameter.spec) is parameter_cls:
                return resolver(parameter, value)

        raise ResolutionError(f"No resolver for parameter {parameter}")


resolvers: Resolvers = Resolvers()


@resolvers(Param)
def resolve_param(
    parameter: Parameter[Param], value: Union[Any, MissingType] = Missing, /
) -> Any:
    if value is not Missing:
        return value
    if parameter.spec.has_default():
        return parameter.spec.get_default()
    else:
        raise ResolutionError("No value provided and parameter has no default")

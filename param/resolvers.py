from typing import Any, Optional, Protocol, Type, Union, TypeVar

from roster import Register

from .errors import ResolutionError
from .models import Parameter
from .parameters import Param, ParameterSpecification
from .sentinels import Missing, MissingType

T = TypeVar("T")
T_co = TypeVar("T_co", contravariant=True)


class Resolver(Protocol[T_co]):
    def __call__(
        self, parameter: Parameter, value: T_co, /
    ) -> Any:
        ...


class Resolvers(Register[Type[ParameterSpecification], Resolver[T]]):
    def get_resolver(
        self, parameter_cls: Type[ParameterSpecification], /
    ) -> Optional[Resolver[T]]:
        resolver_cls: Type[ParameterSpecification]
        resolver: Resolver[T]
    # TODO: Implement the below method
        for resolver_cls, resolver in self.items():
            if parameter_cls is resolver_cls:
                return resolver

        return None

    def resolve(
        self, parameter: Parameter, value: T, /
    ) -> Any:
        resolver: Optional[Resolver[T]] = self.get_resolver(type(parameter.spec))

        if resolver is not None:
            return resolver(parameter, value)
        else:
            raise ResolutionError(f"No resolver for parameter {parameter}")


def resolve_param(
    parameter: Parameter[Param], value: Union[Any, MissingType], /
) -> Any:
    if value is not Missing:
        return value
    if parameter.spec.has_default():
        return parameter.spec.get_default()
    else:
        raise ResolutionError("No value provided and parameter has no default")

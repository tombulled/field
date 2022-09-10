from typing import Any, Optional, Protocol, Type, Union, TypeVar

from roster import Register

from .errors import ResolutionError
from .models import Parameter
from .parameters import Param, ParameterSpecification
from .sentinels import Missing, MissingType

C = TypeVar("C")
C_co = TypeVar("C_co", contravariant=True)


class Resolver(Protocol[C_co]):
    def __call__(
        self, parameter: Parameter, context: C_co, value: Union[Any, MissingType], /
    ) -> Any:
        ...


class Resolvers(Register[Type[ParameterSpecification], Resolver[C]]):
    def get_resolver(
        self, parameter_cls: Type[ParameterSpecification], /
    ) -> Optional[Resolver[C]]:
        return self.get(parameter_cls)

    def resolve(
        self, parameter: Parameter, context: C, value: Union[Any, MissingType], /
    ) -> Any:
        resolver: Optional[Resolver[C]] = self.get_resolver(type(parameter.spec))

        if resolver is not None:
            return resolver(parameter, context, value)
        else:
            raise ResolutionError(f"No resolver for parameter {parameter}")


def resolve_param(
    parameter: Parameter[Param], context: None, value: Union[Any, MissingType], /
) -> Any:
    if value is not Missing:
        return value
    if parameter.spec.has_default():
        return parameter.spec.get_default()
    else:
        raise ResolutionError("No value provided and parameter has no default")

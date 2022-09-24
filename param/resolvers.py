from typing import Any, Callable, Protocol, Type, TypeVar, Union

from roster import Register

from .errors import ResolutionError
from .models import Parameter
from .parameters import Param, ParameterSpecification
from .sentinels import Missing, MissingType

R = TypeVar("R", bound=Callable)


class Resolver(Protocol):
    def __call__(self, parameter: Parameter, value: Union[Any, MissingType], /) -> Any:
        ...


class Resolvers(Register[Type[ParameterSpecification], R]):
    pass


RESOLVERS: Resolvers[Resolver] = Resolvers()


@RESOLVERS(Param)
def resolve_param(
    parameter: Parameter[Param], value: Union[Any, MissingType], /
) -> Any:
    if value is not Missing:
        return value
    if parameter.default.has_default():
        return parameter.default.get_default()
    else:
        raise ResolutionError("No value provided and parameter has no default")

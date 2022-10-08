from typing import Any, Callable, Protocol, Type, TypeVar

from roster import Register

from .errors import ResolutionError
from .models import Resolvable
from .parameters import Param, ParameterSpecification
from .sentinels import Missing

R = TypeVar("R", bound=Callable)


class Resolver(Protocol):
    def __call__(self, resolvable: Resolvable, /) -> Any:
        ...


class Resolvers(Register[Type[ParameterSpecification], R]):
    pass


RESOLVERS: Resolvers[Resolver] = Resolvers()


@RESOLVERS(Param)
def resolve_param(resolvable: Resolvable[Param], /) -> Any:
    if resolvable.argument is not Missing:
        return resolvable.argument
    elif resolvable.specification.has_default():
        return resolvable.specification.get_default()
    else:
        raise ResolutionError("No value provided and parameter has no default")

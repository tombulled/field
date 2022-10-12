from typing import Any, Callable, Protocol, Type, TypeVar

from roster import Register

from .models import Resolvable
from .parameters import Param

R = TypeVar("R", bound=Callable)


class Resolver(Protocol):
    def __call__(self, resolvable: Resolvable, /) -> Any:
        ...


class Resolvers(Register[Type[Param], R]):
    pass


RESOLVERS: Resolvers[Resolver] = Resolvers()


@RESOLVERS(Param)
def resolve_param(resolvable: Resolvable[Param], /) -> Any:
    return resolvable.argument

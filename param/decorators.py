import functools
from typing import Callable, TypeVar

from typing_extensions import ParamSpec

from .manager import ParameterManager
from .models import Arguments, BoundArguments
from .resolvers import resolvers

PS = ParamSpec("PS")
RT = TypeVar("RT")

MANAGER: ParameterManager = ParameterManager(resolvers=resolvers)


def params(func: Callable[PS, RT], /) -> Callable[PS, RT]:
    @functools.wraps(func)
    def wrapper(*args: PS.args, **kwargs: PS.kwargs) -> RT:
        arguments: Arguments = Arguments(args=args, kwargs=kwargs)

        bound_arguments: BoundArguments = MANAGER.get_arguments(func, arguments)

        return bound_arguments.call(func)

    return wrapper

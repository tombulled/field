import functools
from typing import Callable, TypeVar

from typing_extensions import ParamSpec

from .api import get_arguments
from .models import Arguments, BoundArguments

PS = ParamSpec("PS")
RT = TypeVar("RT")


def params(func: Callable[PS, RT], /) -> Callable[PS, RT]:
    @functools.wraps(func)
    def wrapper(*args: PS.args, **kwargs: PS.kwargs) -> RT:
        arguments: Arguments = Arguments(args=args, kwargs=kwargs)

        bound_arguments: BoundArguments = get_arguments(func, arguments)

        return bound_arguments.call(func)

    return wrapper

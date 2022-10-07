import functools
from typing import Callable, TypeVar

from typing_extensions import ParamSpec

from .api import get_arguments
from .models import Arguments, BoundArguments

PS = ParamSpec("PS")
RT = TypeVar("RT")


def params(func: Callable[PS, RT], /) -> Callable[PS, RT]:
    is_static_method: bool = False
    is_class_method: bool = False

    if isinstance(func, classmethod):
        is_class_method = True

        func = func.__func__
    elif isinstance(func, staticmethod):
        is_static_method = True

        func = func.__func__

    @functools.wraps(func)
    def wrapper(*args: PS.args, **kwargs: PS.kwargs) -> RT:
        arguments: Arguments = Arguments(args=args, kwargs=kwargs)

        bound_arguments: BoundArguments = get_arguments(func, arguments)

        return bound_arguments.call(func)

    if is_class_method:
        return classmethod(wrapper)
    elif is_static_method:
        return staticmethod(wrapper)
    else:
        return wrapper

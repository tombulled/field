from typing import Callable, Dict, TypeVar

from typing_extensions import ParamSpec

from .manager import ParameterManager, ParamManager
from .models import Arguments, BoundArguments, Parameter
from .typing import AnyCallable

PS = ParamSpec("PS")
RT = TypeVar("RT")

MANAGER: ParameterManager = ParamManager()


def get_parameters(func: AnyCallable, /) -> Dict[str, Parameter]:
    return MANAGER.get_parameters(func)


def get_arguments(func: AnyCallable, arguments: Arguments) -> BoundArguments:
    return MANAGER.get_arguments(func, arguments)


def params(func: Callable[PS, RT], /) -> Callable[PS, RT]:
    return MANAGER.params(func)

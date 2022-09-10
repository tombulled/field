from typing import Callable, Dict

from .manager import ParameterManager, ParamManager
from .models import Arguments, BoundArguments, Parameter

MANAGER: ParameterManager = ParamManager()


def get_params(func: Callable, /) -> Dict[str, Parameter]:
    return MANAGER.get_params(func)


def get_arguments(func: Callable, arguments: Arguments) -> BoundArguments:
    return MANAGER.get_arguments(func, arguments)

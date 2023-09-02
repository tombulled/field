import inspect
from typing import Callable, Mapping, Sequence, TypeVar

from typing_extensions import ParamSpec

from .manager import ParameterManager, ParamManager
from .models import Arguments, BoundArguments, Parameter
from .typing import AnyCallable

__all__: Sequence[str] = ("get_parameters", "get_arguments", "params")

PS = ParamSpec("PS")
RT = TypeVar("RT")

MANAGER: ParameterManager = ParamManager()


def get_parameters(func: AnyCallable, /) -> Mapping[str, Parameter]:
    return {
        parameter.name: Parameter.from_parameter(parameter)
        for parameter in inspect.signature(func).parameters.values()
    }


def get_arguments(func: AnyCallable, arguments: Arguments) -> BoundArguments:
    return MANAGER.get_arguments(func, arguments)


def params(func: Callable[PS, RT], /) -> Callable[PS, RT]:
    return MANAGER.params(func)

import inspect
from typing import Mapping, Sequence

from .models import Parameter
from .typing import AnyCallable

__all__: Sequence[str] = ("get_parameters",)


def get_parameters(func: AnyCallable, /) -> Mapping[str, Parameter]:
    return {
        parameter.name: Parameter.from_parameter(parameter)
        for parameter in inspect.signature(func).parameters.values()
    }

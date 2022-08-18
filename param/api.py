import inspect
from typing import Any, Callable, Dict, List, Tuple, TypeVar
from typing_extensions import ParamSpec
import functools
from inspect import BoundArguments, Signature, Parameter
from .param import Param

PS = ParamSpec("PS")
RT = TypeVar("RT")

def enrich(parameter: Parameter, argument: Any) -> Any:
    if not isinstance(argument, Param):
        return argument

    if not argument.has_default():
        raise ValueError(f"missing argument: {parameter.name}")

    return argument.default

def get_arguments(func: Callable[..., Any], args: Tuple[Any], kwargs: Dict[str, Any]) -> Tuple[Tuple[Any], Dict[str, Any]]:
    signature: Signature = inspect.signature(func)

    bound_arguments: BoundArguments = signature.bind(*args, **kwargs)

    bound_arguments.apply_defaults()

    new_args: List[Any] = list(bound_arguments.args)
    new_kwargs: Dict[str, Any] = dict(bound_arguments.kwargs)

    index: int
    arg: Any
    for index, arg in enumerate(bound_arguments.args):
        aparam: Parameter = list(signature.parameters.values())[index]
        new_args[index] = enrich(aparam, arg)

    argument_name: str
    argument: Any
    for argument_name, argument in bound_arguments.kwargs.items():
        bparam: Parameter = signature.parameters[argument_name]

        new_kwargs[argument_name] = enrich(bparam, argument)

    return (new_args, new_kwargs)


def params(func: Callable[PS, RT], /) -> Callable[PS, RT]:
    @functools.wraps(func)
    def wrapper(*args: PS.args, **kwargs: PS.kwargs) -> RT:
        new_args: Tuple[Any]
        new_kwargs: Dict[str, Any]
        new_args, new_kwargs = get_arguments(func, args, kwargs)

        return func(*new_args, **new_kwargs)

    return wrapper

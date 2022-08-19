import inspect
from typing import Any, Callable, Dict, List, Tuple, TypeVar
from typing_extensions import ParamSpec
import functools
from inspect import BoundArguments, Signature
from .param import Param
from .models import Parameter, Arguments
from .enums import ParameterType
from .sentinels import Missing

PS = ParamSpec("PS")
RT = TypeVar("RT")


def enrich(parameter: inspect.Parameter, argument: Any) -> Any:
    if not isinstance(argument, Param):
        return argument

    if not argument.has_default():
        raise ValueError(f"missing argument: {parameter.name}")

    return argument.default


def get_arguments(
    func: Callable[..., Any], args: Tuple[Any], kwargs: Dict[str, Any]
) -> Arguments:
    signature: Signature = inspect.signature(func)

    bound_arguments: BoundArguments = signature.bind(*args, **kwargs)

    bound_arguments.apply_defaults()

    arguments: Dict[str, Any] = dict(bound_arguments.arguments)
    new_args: List[Any] = list(bound_arguments.args)
    new_kwargs: Dict[str, Any] = dict(bound_arguments.kwargs)

    index: int
    arg: Any
    for index, arg in enumerate(bound_arguments.args):
        aparam: inspect.Parameter = list(signature.parameters.values())[index]
        new_args[index] = enrich(aparam, arg)

    argument_name: str
    argument: Any
    for argument_name, argument in bound_arguments.kwargs.items():
        bparam: inspect.Parameter = signature.parameters[argument_name]

        new_kwargs[argument_name] = enrich(bparam, argument)

    return Arguments(args=tuple(new_args), kwargs=new_kwargs, arguments=arguments)


def parse(value: Any, /) -> Any:
    if value is inspect._empty:
        return Missing

    return value


def get_params(func: Callable[PS, RT], /) -> Dict[str, Parameter]:
    params: Dict[str, Parameter] = {}

    parameter: inspect.Parameter
    for parameter in inspect.signature(func).parameters.values():
        spec: Param = (
            parameter.default
            if isinstance(parameter.default, Param)
            else Param(default=parse(parameter.default))
        )

        param: Parameter = Parameter(
            name=parameter.name,
            annotation=parse(parameter.annotation),
            type=getattr(ParameterType, parameter.kind.name),
            spec=spec,
        )

        params[parameter.name] = param

    return params


def params(func: Callable[PS, RT], /) -> Callable[PS, RT]:
    @functools.wraps(func)
    def wrapper(*args: PS.args, **kwargs: PS.kwargs) -> RT:
        arguments: Arguments = get_arguments(func, args, kwargs)

        return func(*arguments.args, **arguments.kwargs)

    return wrapper

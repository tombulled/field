import functools
import inspect
from inspect import BoundArguments, Signature
from typing import Any, Callable, Dict, List, Tuple, TypeVar

from typing_extensions import ParamSpec

from .enums import ParameterType
from .models import Arguments, Parameter, ParameterSpecification
from .sentinels import Missing

PS = ParamSpec("PS")
RT = TypeVar("RT")


def _enrich(parameter: inspect.Parameter, argument: Any) -> Any:
    if not isinstance(argument, ParameterSpecification):
        return argument

    if not argument.has_default():
        raise ValueError(f"missing argument: {parameter.name}")

    return argument.default


def get_arguments(
    func: Callable[..., Any], args: Tuple[Any, ...], kwargs: Dict[str, Any]
) -> Arguments:
    signature: Signature = inspect.signature(func)

    bound_arguments: BoundArguments = signature.bind(*args, **kwargs)

    bound_arguments.apply_defaults()

    arguments: Dict[str, Any] = {}
    new_args: List[Any] = list(bound_arguments.args)
    new_kwargs: Dict[str, Any] = dict(bound_arguments.kwargs)

    index: int
    arg: Any
    for index, arg in enumerate(bound_arguments.args):
        aparam: inspect.Parameter = list(signature.parameters.values())[index]
        new_args[index] = _enrich(aparam, arg)
        arguments[aparam.name] = _enrich(aparam, arg)

    argument_name: str
    argument: Any
    for argument_name, argument in bound_arguments.kwargs.items():
        bparam: inspect.Parameter = signature.parameters[argument_name]

        new_kwargs[argument_name] = _enrich(bparam, argument)
        arguments[argument_name] = _enrich(bparam, argument)

    return Arguments(args=tuple(new_args), kwargs=new_kwargs, arguments=arguments)


def _parse(value: Any, /) -> Any:
    if value is inspect._empty:
        return Missing

    return value


def get_params(func: Callable[PS, RT], /) -> Dict[str, Parameter]:
    params: Dict[str, Parameter] = {}

    parameter: inspect.Parameter
    for parameter in inspect.signature(func).parameters.values():
        spec: ParameterSpecification = (
            parameter.default
            if isinstance(parameter.default, ParameterSpecification)
            else ParameterSpecification(default=_parse(parameter.default))
        )

        param: Parameter = Parameter(
            name=parameter.name,
            annotation=_parse(parameter.annotation),
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

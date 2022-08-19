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


def _enrich(arguments: Dict[str, Any], /) -> Dict[str, Any]:
    enriched_arguments: Dict[str, Any] = {}

    argument_name: str
    argument: Any
    for argument_name, argument in arguments.items():
        if not isinstance(argument, ParameterSpecification):
            enriched_arguments[argument_name] = argument
        elif not argument.has_default():
            raise ValueError(f"missing argument: {argument_name}")
        else:
            enriched_arguments[argument_name] = argument.default

    return enriched_arguments


def get_arguments(
    func: Callable[..., Any], args: Tuple[Any, ...], kwargs: Dict[str, Any]
) -> Arguments:
    signature: Signature = inspect.signature(func)

    bound_arguments: BoundArguments = signature.bind(*args, **kwargs)

    bound_arguments.apply_defaults()

    parameters: Dict[str, Parameter] = get_params(func)

    keyed_args: Dict[str, Any] = {
        list(signature.parameters.values())[index].name: arg
        for index, arg in enumerate(bound_arguments.args)
    }

    new_args: Dict[str, Any] = _enrich(keyed_args)
    new_kwargs: Dict[str, Any] = _enrich(bound_arguments.kwargs)

    return Arguments(
        args=tuple(new_args.values()),
        kwargs=new_kwargs,
        arguments={**new_args, **new_kwargs},
    )


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

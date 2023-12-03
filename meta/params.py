import functools
import inspect
from dataclasses import dataclass
from typing import Any, Callable, Mapping, MutableMapping, Sequence, TypeVar

from arguments import Arguments, BoundArguments
from typing_extensions import ParamSpec

from .api import MetadataManager, ParameterMetadataManager

__all__: Sequence[str] = ("Params",)

M = TypeVar("M")
R = TypeVar("R")

PS = ParamSpec("PS")
RT = TypeVar("RT")


@dataclass
class Params(ParameterMetadataManager[M, R]):
    metadata_manager: MetadataManager[M, R]

    def wrap(self, func: Callable[PS, RT], /) -> Callable[PS, RT]:
        @functools.wraps(func)
        def wrapper(*args: PS.args, **kwargs: PS.kwargs) -> RT:
            arguments: Arguments = Arguments(*args, **kwargs)

            resolved_arguments: Arguments = self.resolve(func, arguments)

            bound_arguments: BoundArguments = resolved_arguments.bind(func)

            return bound_arguments.call(func)

        return wrapper

    def resolve(self, func: Callable[..., Any], arguments: Arguments) -> Arguments:
        bound_arguments: BoundArguments = arguments.bind(func)

        parameters: Mapping[str, inspect.Parameter] = inspect.signature(func).parameters

        args: MutableMapping[str, Any] = {}
        kwargs: MutableMapping[str, Any] = {}

        parameter: inspect.Parameter
        for parameter in parameters.values():
            argument: Any = bound_arguments.get(parameter.name)
            resolved_argument: Any = self.resolve_parameter(parameter, argument)

            if parameter.name in bound_arguments.kwargs:
                kwargs[parameter.name] = resolved_argument
            else:
                args[parameter.name] = resolved_argument

        return Arguments(*args.values(), **kwargs)

    def resolve_parameter(self, parameter: inspect.Parameter, argument: Any) -> R:
        metadatas: Sequence[M] = self.metadata_manager.parse(parameter.annotation)

        resolved_argument: Any = argument

        metadata: Any
        for metadata in metadatas:
            resolved_argument = self.metadata_manager.resolve(argument, metadata)

        return resolved_argument

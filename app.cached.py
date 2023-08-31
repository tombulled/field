import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, TypeVar, Union

from param import Param
from param.errors import ResolutionError
from param.manager import ParameterManager
from param.models import Arguments, Parameter
from param.parameters import Param as ParamModel
from param.parameters import ParameterSpecification
from param.resolvers import Resolvers
from param.sentinels import Missing, MissingType
from param.utils import parse_parameter_value

"""
* Support the scenario where need to resolve multiple at once (e.g. Body)
* Support "Depends" which needs access to the manager

@get
def foo(user: User = Body(), item: Item = Body())
"""

T = TypeVar("T")


@dataclass
class Context:
    manager: ParameterManager
    parameters: List[Parameter]
    dependency_cache: Dict[Callable, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Dependency(ParameterSpecification):
    dependency: Callable[[], T]


@dataclass(frozen=True)
class BodyParam(ParameterSpecification):
    pass


def Depends(dependency: Callable[[], T]) -> Any:
    return Dependency(dependency=dependency)


def Body() -> Any:
    return BodyParam()


resolvers: Resolvers[Context] = Resolvers()


@resolvers(Dependency)
def resolve_dependency(
    parameter: Parameter[Dependency],
    context: Context,
    value: Union[Any, MissingType],
    /,
) -> Any:
    if value is not Missing:
        return value

    if parameter.spec.dependency in context.dependency_cache:
        return context.dependency_cache[parameter.spec.dependency]

    resolved_value: Any = context.manager.get_arguments(
        parameter.spec.dependency, Arguments()
    ).call(parameter.spec.dependency)

    context.dependency_cache[parameter.spec.dependency] = resolved_value

    return resolved_value


@resolvers(ParamModel)
def resolve_param(
    parameter: Parameter[ParamModel],
    context: Context,
    value: Union[Any, MissingType],
    /,
):
    if value is not Missing:
        return value
    elif parameter.spec.has_default():
        return parameter.spec.get_default()
    else:
        raise ResolutionError("Param has no value or default")


@resolvers(Body)
def resolve_body(
    parameter: Parameter[BodyParam], context: Context, value: Union[Any, MissingType], /
):
    ...


def some_dependency(name: str = Param(default="sam")) -> str:
    return name


def foo(
    foo: int,
    bar: str = Depends(dependency=some_dependency),
    baz: str = Depends(dependency=some_dependency),
):
    ...


@dataclass
class DependencyParameterManager(ParameterManager[Context]):
    resolvers: Resolvers[Context]

    # NOTE: Inference will require more information (e.g. RequestOptions)
    def infer_parameter(
        self, parameter: inspect.Parameter, /
    ) -> ParameterSpecification:
        return Param(default=_parse(parameter.default))

    def build_contexts(
        self, parameters: Dict[str, Parameter], arguments: Dict[str, Any]
    ) -> Dict[str, Context]:
        dependency_cache: dict = {}

        return {
            parameter: Context(
                manager=self,
                parameters=list(parameters.values()),
                dependency_cache=dependency_cache,
            )
            for parameter in parameters
        }

    # def resolve_parameters(
    #     self, parameters: Dict[str, Parameter], arguments: Dict[str, Any], /
    # ) -> Dict[str, Any]:
    #     dependency_cache: dict = {}

    #     arguments = {
    #         parameter: Context(
    #             manager=self,
    #             parameters=list(parameters.values()),
    #             dependency_cache=dependency_cache,
    #         )
    #         for parameter in parameters
    #     }

    #     return super().resolve_parameters(parameters, arguments)


manager: ParameterManager = DependencyParameterManager(resolvers=resolvers)


d = manager.get_arguments(foo, Arguments(args=(1,)))
d2 = manager.get_arguments(foo, Arguments(args=(1, "bar")))
# d2 = manager.get_arguments(foo, Arguments(args=(1,)))
# d2 = manager.get_arguments(foo, Arguments(args=("bar",)))

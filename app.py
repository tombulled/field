from dataclasses import dataclass, field
from typing import Any, Dict, Union

from param.api import MANAGER
from param.errors import ResolutionError
from param.models import Arguments, Parameter
from param.parameters import Param
from param.resolvers import Resolvers
from param.sentinels import Missing, MissingType

get_arguments = MANAGER.get_arguments
get_params = MANAGER.get_params

"""
Composer:
    Needs: RequestOptions, user-provided value

Resolver:
    Needs: RequestOptions, Response
"""


@dataclass
class Request:
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class QueryParam(Param):
    pass


def Query(default: Union[str, MissingType] = Missing) -> Any:
    return QueryParam(default=default)


@MANAGER.resolvers(QueryParam)
def resolve_query(
    parameter: Parameter[QueryParam], value: Union[Any, MissingType] = Missing, /
) -> Any:
    if value is not Missing:
        return value
    if parameter.spec.has_default():
        return parameter.spec.get_default()
    else:
        raise ResolutionError("No value provided and parameter has no default")


def foo(bar: str = Query(default="default")):
    ...


d = get_arguments(foo, Arguments())
d2 = get_arguments(foo, Arguments(args=("bar",)))

from dataclasses import dataclass, field
from typing import Any

from pydantic.fields import UndefinedType

import param.parameters
from param import (
    Param,
    Parameter,
    ParameterManager,
    Resolvable,
    Resolver,
    Resolvers,
    params,
)
from param.resolvers import resolve_field_info


@dataclass
class ParamManager(ParameterManager[Resolver]):
    resolvers: Resolvers[Resolver] = field(
        default_factory=lambda: Resolvers({param.parameters.Param: resolve_field_info})
    )

    def resolve(self, resolvable: Resolvable) -> Any:
        return self.get_resolver(type(parameter.default))(parameter, argument)


pm = ParamManager()


@params
def foo(age: int, name: str = "sam", food: str = Param(default="Pizza!")) -> dict:
    return dict(
        age=age,
        name=name,
        food=food,
    )


p = pm.get_parameters(foo)

d = foo(123)

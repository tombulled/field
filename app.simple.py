from dataclasses import dataclass, field
from param import Param, ParameterManager, Parameter, Resolvers, Resolver, params, Resolvable
from pydantic.fields import UndefinedType
from param.resolvers import resolve_param
import param.parameters
from typing import Union, Any

@dataclass
class ParamManager(ParameterManager[Resolver]):
    resolvers: Resolvers[Resolver] = field(default_factory=lambda: Resolvers({
        param.parameters.Param: resolve_param
    }))

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
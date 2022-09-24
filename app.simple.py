from param import Param, ParameterManager, Parameter, Resolvers, Resolver, params
from param.sentinels import MissingType
from param.resolvers import resolve_param
import param.parameters
from typing import Union, Any

class ParamManager(ParameterManager[Resolver]):
    resolvers: Resolvers[Resolver] = Resolvers({
        param.parameters.Param: resolve_param
    })

    def resolve(self, parameter: Parameter, argument: Union[Any, MissingType]) -> Any:
        return self.get_resolver(type(parameter.default))(parameter, argument)

pm = ParamManager()


@params
def foo(age: int, name: str = "sam", food: str = Param(default="Pizza!")) -> dict:
    return dict(
        age=age,
        name=name,
        food=food,
    )

p = pm.get_params(foo)

d = foo(123)
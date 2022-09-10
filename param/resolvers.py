from typing import Any, Optional, Protocol, Type, Union

from roster import Register

from .errors import ResolutionError
from .models import Parameter
from .parameters import Param, ParameterSpecification
from .sentinels import Missing, MissingType


# NOTE: Change signature to (manager: ParameterManager, parameters: Sequence[Parameter], arguments: Dict[str, Any])
# NOTE: Depends could just access the MANAGER instance? (likely to cause a dependency hell conflict)
class Resolver(Protocol):
    def __call__(
        self, parameter: Parameter, value: Union[Any, MissingType] = Missing, /
    ) -> Any:
        ...


class Resolvers(Register[Type[ParameterSpecification], Resolver]):
    def get_resolver(
        self, parameter_cls: Type[ParameterSpecification], /
    ) -> Optional[Resolver]:
        resolver_cls: Type[ParameterSpecification]
        resolver: Resolver
    # TODO: Implement the below method
        for resolver_cls, resolver in self.items():
            if parameter_cls is resolver_cls:
                return resolver

        return None

    def resolve(
        self, parameter: Parameter, value: Union[Any, MissingType] = Missing, /
    ) -> Any:
        resolver: Optional[Resolver] = self.get_resolver(type(parameter.spec))

        if resolver is not None:
            return resolver(parameter, value)
        else:
            raise ResolutionError(f"No resolver for parameter {parameter}")


def resolve_param(
    parameter: Parameter[Param], value: Union[Any, MissingType] = Missing, /
) -> Any:
    if value is not Missing:
        return value
    if parameter.spec.has_default():
        return parameter.spec.get_default()
    else:
        raise ResolutionError("No value provided and parameter has no default")

from typing import Any, Protocol, Sequence, Type, TypeVar, Union

from roster import Register
from pydantic.fields import FieldInfo

from .errors import ResolutionError
from .sentinels import Undefined, UndefinedType

__all__: Sequence[str] = ("Resolver", "Resolvers", "RESOLVERS", "resolve_param")


class Resolver(Protocol):
    def __call__(self, param: FieldInfo, argument: Union[Any, UndefinedType]) -> Any:
        ...


R = TypeVar("R", bound=Resolver)


class Resolvers(Register[Type[FieldInfo], R]):
    pass


RESOLVERS: Resolvers[Resolver] = Resolvers()


@RESOLVERS(FieldInfo)
def resolve_param(param: FieldInfo, argument: Any) -> Any:
    if argument is not Undefined:
        return argument

    default: Any = param.get_default()

    if default is not Undefined:
        return default

    raise ResolutionError("No value provided and parameter has no default")

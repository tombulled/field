from typing import (
    Any,
    Callable,
    Dict,
    Protocol,
    Sequence,
    Type,
    TypeVar,
)

from pydantic.fields import FieldInfo

from .errors import ResolutionError
from .sentinels import Undefined
from .typing import AnyOrUndefined

__all__: Sequence[str] = (
    "Resolver",
    "Resolvers",
    "RESOLVERS",
    "resolve_field_info",
)

M = TypeVar("M")
M_cont = TypeVar("M_cont", contravariant=True)


class Resolver(Protocol[M_cont]):
    def __call__(self, metadata: M_cont, argument: AnyOrUndefined) -> Any:
        ...


class Resolvers(Dict[Type[M], Resolver[M]]):
    def __call__(
        self, metadata_cls: Type[M], /
    ) -> Callable[[Resolver[M]], Resolver[M]]:
        def wrapper(resolver: Resolver[M], /) -> Resolver[M]:
            self[metadata_cls] = resolver

            return resolver

        return wrapper


RESOLVERS: Resolvers[FieldInfo] = Resolvers()


@RESOLVERS(FieldInfo)
def resolve_field_info(metadata: FieldInfo, argument: Any) -> Any:
    # TODO: Validation should also be carried out

    if argument is not Undefined:
        return argument

    default: Any = metadata.get_default()

    if default is not Undefined:
        return default

    raise ResolutionError("No value provided and parameter has no default")

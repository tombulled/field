import functools
from typing import Callable, Mapping, MutableMapping, Optional, Sequence, Type, TypeVar

from arguments import Arguments
from typing_extensions import ParamSpec, TypeAlias

from .resolver import Resolver

__all__: Sequence[str] = ("Params",)

M = TypeVar("M")
R = TypeVar("R")

PS = ParamSpec("PS")
RT = TypeVar("RT")

Resolvers: TypeAlias = Mapping[type, Resolver]
MutableResolvers: TypeAlias = MutableMapping[type, Resolver]


class Params:
    resolvers: MutableResolvers

    def __init__(
        self,
        resolvers: Optional[Resolvers] = None,
        /,
    ) -> None:
        self.resolvers = {**resolvers} if resolvers is not None else {}

    def __call__(self, func: Callable[PS, RT], /) -> Callable[PS, RT]:
        @functools.wraps(func)
        def wrapper(*args: PS.args, **kwargs: PS.kwargs) -> RT:
            arguments: Arguments = Arguments(*args, **kwargs)

            print(f"Arguments: {arguments!r}")

            raise NotImplementedError

        return wrapper

    def resolver(self, metadata_cls: Type[M], /):  # TODO: Type me
        def wrapper(resolver: Resolver[M, R], /) -> Resolver[M, R]:
            self.resolvers[metadata_cls] = resolver

            return resolver

        return wrapper

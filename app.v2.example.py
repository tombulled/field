from abc import abstractmethod
from typing import Any, TypeVar

from typing_extensions import Annotated

from param import params
from param.errors import ResolutionError
from param.resolvers import Resolver
from param.sentinels import Missing


class Upper:
    pass


class Lower:
    pass


class Title:
    pass


R = TypeVar("R")
M_cont = TypeVar("M_cont", contravariant=True)


class StrResolver(Resolver[M_cont, R]):
    def __call__(self, metadata: M_cont, argument: Any) -> R:
        if argument is Missing:
            raise ResolutionError

        if not isinstance(argument, str):
            raise ResolutionError

        return self.resolve(metadata, argument)

    @abstractmethod
    def resolve(self, metadata: M_cont, argument: str) -> R:
        raise NotImplementedError


class UpperResolver(StrResolver[str]):
    def resolve(self, _, argument: str) -> str:
        return argument.upper()


class LowerResolver(StrResolver[str]):
    def resolve(self, _, argument: str) -> str:
        return argument.lower()


class TitleResolver(StrResolver[str]):
    def resolve(self, _, argument: str) -> str:
        return argument.title()


def resolve_upper(_, argument: str) -> str:
    return argument.upper()


Name = Annotated[str, Upper()]


@params
def greet(name: Name, /) -> str:
    return f"Hello, {name}"


assert greet("bob") == "Hello, BOB"

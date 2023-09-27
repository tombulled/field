from dataclasses import dataclass
from typing import Annotated, Callable, TypeVar
from param import Params
from param.resolver import Resolvers

T = TypeVar("T")


@dataclass
class Parse:
    parser: Callable[[T], T]

    @staticmethod
    def resolve(metadata: "Parse", value: T, /) -> T:
        return metadata.parser(value)


def to_upper(_, string: str) -> str:
    return string.upper()


def to_title(_, string: str) -> str:
    return string.title()


def test_Params_init() -> None:
    resolvers: Resolvers = {str: to_upper}

    assert Params().resolvers == {}
    assert Params(resolvers).resolvers == resolvers
    assert Params(resolvers).resolvers is not resolvers


def test_Params_repr() -> None:
    resolvers: Resolvers = {str: to_upper}

    assert repr(Params()) == "Params({})"
    assert repr(Params(resolvers)) == f"Params({resolvers!r})"


def test_Params_call() -> None:
    params: Params = Params({Parse: Parse.resolve})

    @params
    def greet(name: Annotated[str, Parse(str.title)]) -> str:
        return f"Hello, {name}!"

    assert greet("BOB dylan") == "Hello, Bob Dylan!"

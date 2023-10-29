from dataclasses import dataclass
import inspect
from typing import Any, Callable, Generic, TypeVar
from typing_extensions import Annotated

from arguments import Arguments
import pytest
from param import Params
from param.resolver import Resolvers
from param.errors import ResolutionError

T = TypeVar("T")


@dataclass
class Parse(Generic[T]):
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


def test_Params_resolver() -> None:
    params: Params = Params()

    @dataclass
    class Punctuate:
        punctation: str

    @params.resolver(Punctuate)
    def resolve_punctuate(metadata: Punctuate, argument: Any) -> str:
        if not isinstance(argument, str):
            raise TypeError(f"Cannot punctuate argument of type {type(argument)!r}")

        return argument + metadata.punctation

    @params
    def greet(name: Annotated[str, Punctuate("!")], /) -> str:
        return f"Hello, {name}"

    assert greet("Bob") == "Hello, Bob!"


def test_Params_get_resolver() -> None:
    params: Params = Params({Parse: Parse.resolve})

    assert params.get_resolver(Parse(str.upper)) is Parse.resolve
    assert params.get_resolver("other metadata") is None


def test_Params_can_resolve() -> None:
    params: Params = Params({Parse: Parse.resolve})

    assert params.can_resolve(Parse(str.upper))
    assert not params.can_resolve("other metadata")


def test_Params_resolve_metadata() -> None:
    params: Params = Params({Parse: Parse.resolve})

    assert params.resolve_metadata(Parse(str.upper), "bob") == "BOB"

    with pytest.raises(ResolutionError):
        params.resolve_metadata("other metadata", "value")


def test_Params_get_metadata() -> None:
    params: Params = Params({Parse: Parse.resolve})
    metadata: Parse = Parse(str.upper)

    assert params.get_metadata(Annotated[Any, "other metadata", metadata]) == [metadata]


def test_Params_get_parameter_metadata() -> None:
    params: Params = Params({Parse: Parse.resolve})
    metadata: Parse = Parse(str.upper)
    parameter: inspect.Parameter = inspect.Parameter(
        name="name",
        kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
        annotation=Annotated[Any, "other metadata", metadata],
    )

    assert params.get_parameter_metadata(parameter) == [metadata]


def test_Params_resolve() -> None:
    params: Params = Params({Parse: Parse.resolve})

    def greet(name: Annotated[str, Parse(str.title)], /) -> str:
        return f"Hello, {name}"

    assert params.resolve(greet, Arguments("bob dylan")) == Arguments("Bob Dylan")

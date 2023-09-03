from dataclasses import dataclass

from typing_extensions import Annotated

from param import Missing, Params
from param.models import Arguments
from param.typing import Argument

params: Params = Params()


class Upper:
    pass


@dataclass
class Punctuate:
    punctation: str


EXCLAIM: Punctuate = Punctuate("!")


@params.resolver(Upper)
def resolve_upper(_: Upper, argument: Argument) -> str:
    if argument is Missing or not isinstance(argument, str):
        raise Exception

    return argument.upper()


@params.resolver(Punctuate)
def resolve_punctuate(metadata: Punctuate, argument: Argument) -> str:
    if argument is Missing or not isinstance(argument, str):
        raise Exception

    return argument + metadata.punctation


Name = Annotated[str, Upper(), EXCLAIM]


@params
def greet(name: Name, /) -> str:
    return f"Hello, {name}"


# assert greet("bob") == "Hello, BOB"

arguments: Arguments = Arguments("bob")

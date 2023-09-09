from dataclasses import dataclass
from typing import Any

from typing_extensions import Annotated

from param import Missing, Params


class Upper:
    pass


params: Params[Upper, str] = Params()


@dataclass
class Punctuate:
    punctation: str


EXCLAIM: Punctuate = Punctuate("!")


@params.resolver(Upper)
def resolve_upper(_, argument: Any) -> str:
    if argument is Missing or not isinstance(argument, str):
        raise Exception

    return argument.upper()


# @params.resolver(Punctuate)
def resolve_punctuate(metadata: Punctuate, argument: Any) -> str:
    if argument is Missing or not isinstance(argument, str):
        raise Exception

    return argument + metadata.punctation


Name = Annotated[str, Upper(), EXCLAIM]


@params
def greet(name: Name = "sally", /) -> str:
    return f"Hello, {name}"


# assert greet("bob") == "Hello, BOB!"

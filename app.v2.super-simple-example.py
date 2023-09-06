from dataclasses import dataclass
from typing import Any

from typing_extensions import Annotated

from param import Params

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

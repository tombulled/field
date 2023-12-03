from dataclasses import dataclass
from typing import Any
from typing_extensions import Annotated

from meta import Meta


@dataclass
class Punctuate:
    punctation: str


meta = Meta()


@meta.resolver(Punctuate)
def resolve_punctuate(metadata: Punctuate, argument: Any) -> str:
    if not isinstance(argument, str):
        raise TypeError(f"Cannot punctuate argument of type {type(argument)!r}")

    return argument + metadata.punctation


@meta
def greet(name: Annotated[str, Punctuate("!")], /) -> str:
    return f"Hello, {name}"


print(greet("Sam"))

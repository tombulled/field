from dataclasses import dataclass
from typing import Any

from typing_extensions import Annotated

from param import Missing, Params
from param.models import Arguments
from param.params import NewParams

new_params: NewParams = NewParams()
params: Params = Params()


class Upper:
    pass


@dataclass
class Punctuate:
    punctation: str


EXCLAIM: Punctuate = Punctuate("!")


@new_params.resolver(Upper)
@params.resolver(Upper)
def resolve_upper(_, argument: Any) -> str:
    if argument is Missing or not isinstance(argument, str):
        raise Exception

    return argument.upper()


@new_params.resolver(Punctuate)
@params.resolver(Punctuate)
def resolve_punctuate(metadata: Punctuate, argument: Any) -> str:
    if argument is Missing or not isinstance(argument, str):
        raise Exception

    return argument + metadata.punctation


Name = Annotated[str, Upper(), EXCLAIM]


@new_params
# @params
def greet(name: Name = "sally", /) -> str:
    return f"Hello, {name}"


# assert greet("bob") == "Hello, BOB"

arguments: Arguments = Arguments("bob")

d = new_params.resolve(greet, arguments)

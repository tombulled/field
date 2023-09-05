from dataclasses import dataclass
from typing import Any

from typing_extensions import Annotated

from param import Missing, Params
from param.params import NewParams
from param.models import Arguments, ResolutionContext

new_params: NewParams = NewParams()
params: Params = Params()


class Upper:
    pass


@dataclass
class Punctuate:
    punctation: str


EXCLAIM: Punctuate = Punctuate("!")


@params.resolver(Upper)
def resolve_upper(_, argument: Any) -> str:
    if argument is Missing or not isinstance(argument, str):
        raise Exception

    return argument.upper()


@params.resolver(Punctuate)
def resolve_punctuate(ctx: ResolutionContext[Punctuate], argument: Any) -> str:
    if argument is Missing or not isinstance(argument, str):
        raise Exception

    return argument + ctx.metadata.punctation

new_params.resolvers.update({
    Upper: resolve_upper,
    Punctuate: resolve_punctuate,
})

Name = Annotated[str, Upper(), EXCLAIM]

@params
def greet(name: Name = "sally", /) -> str:
    return f"Hello, {name}"


# assert greet("bob") == "Hello, BOB"

arguments: Arguments = Arguments("bob")

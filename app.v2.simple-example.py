from typing_extensions import Annotated

from param import Params, Missing
from param.typing import Argument

params: Params = Params()


class Upper:
    pass


@params.resolver(Upper)
def resolve_upper(_: Upper, argument: Argument) -> str:
    if argument is Missing or not isinstance(argument, str):
        raise Exception
    
    return argument.upper()


Name = Annotated[str, Upper()]


@params
def greet(name: Name, /) -> str:
    return f"Hello, {name}"


assert greet("bob") == "Hello, BOB"

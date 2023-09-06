from typing_extensions import Annotated

from param.pydantic import Param, PydanticParams

params = PydanticParams()

Name = Annotated[str, Param()]


@params
def greet(name: Name, /) -> str:
    return f"Hello, {name!r}"

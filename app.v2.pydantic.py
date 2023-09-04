from param import Params
from param.pydantic import PydanticResolver, ParamInfo, Param

from typing_extensions import Annotated

params = Params({ParamInfo: PydanticResolver()})

Name = Annotated[str, Param()]


@params
def greet(name: Name, /) -> str:
    return f"Hello, {name!r}"

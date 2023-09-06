from typing_extensions import Annotated

from param import Params
from param.pydantic import Param, ParamInfo, PydanticResolver

params = Params({ParamInfo: PydanticResolver()})

Name = Annotated[str, Param()]


@params
def greet(name: Name, /) -> str:
    return f"Hello, {name!r}"

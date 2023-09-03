from pydantic import Field
from pydantic.fields import FieldInfo
from typing_extensions import Annotated

from param.enums import ParameterType


def say(message: Annotated[str, Field(default="Hello, World!")]) -> None:
    print(message)

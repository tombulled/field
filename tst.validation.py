from pydantic.fields import Field
from typing_extensions import Annotated

from param.validation import ValidatedFunction


def greet(name: Annotated[str, Field(...)], message: str = Field(default="hello")):
    print(message, name)


def say(message=Field(...)):
    print(message)


def say2(message=Field(default_factory=dict)):
    print(message)


vf = ValidatedFunction(greet)
vfs = ValidatedFunction(say)
vfs2 = ValidatedFunction(say2)

m = vf.model(**vf.bind_arguments(("sam",), {}))
# m2 = vfs.model(**vfs.bind_arguments((), {}))
m3 = vfs2.model(**vfs2.bind_arguments((), {}))

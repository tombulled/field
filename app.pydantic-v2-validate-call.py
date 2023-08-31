from functools import wraps
from typing import Any, Callable, Mapping, TypeVar
from typing_extensions import ParamSpec

from arguments import Arguments

from pydantic import Field, validate_call
from typing_extensions import Annotated

"""
The example below works great for pydantic's `FieldInfo`, but nothing else.

Unless... Pydantic does allow you to create custom types - could these be leveraged?
    Doesn't appear so, at least not easily.

Maybe the custom types should be used *alongside* the pydantic metadata, e.g.:
    Name = Annotated[str, Header(name="x-name"), Len(3)]
Then, pydantic will quite happily validate it, but neoclient can rip out the value.
"""

PS = ParamSpec("PS")
RT = TypeVar("RT")


def resolve(arguments: Mapping[str, Any], /) -> Any:
    return arguments["message"]


def operation(func: Callable[PS, RT], /) -> Callable[PS, RT]:
    @validate_call
    @wraps(func)
    def capture_arguments(*args, **kwargs) -> RT:
        arguments: Mapping[str, Any] = Arguments(*args, **kwargs).bind(func).asdict()

        return resolve(arguments)

    return capture_arguments


@operation
def say(message: Annotated[str, Field(default="Hello, World!")], /) -> str:
    ...

import pytest
from pydantic import ConfigDict, ValidationError
from pydantic.fields import FieldInfo
from typing_extensions import Annotated

from param.pydantic import PydanticResolver


def test_PydanticResolver_default_config() -> None:
    resolver: PydanticResolver = PydanticResolver()

    assert resolver(FieldInfo(), "abc") == "abc"
    assert resolver(FieldInfo(annotation=str), "abc") == "abc"
    assert resolver(FieldInfo(annotation=Annotated[str, "wow"]), "abc") == "abc"

    with pytest.raises(ValidationError):
        resolver(FieldInfo(annotation=int), "abc")

    with pytest.raises(ValidationError):
        resolver(FieldInfo(max_length=1), "abc")


def test_PydanticResolver_config() -> None:
    resolver: PydanticResolver = PydanticResolver(config=ConfigDict(str_max_length=3))

    assert resolver(FieldInfo(annotation=str), "abc") == "abc"

    with pytest.raises(ValidationError):
        resolver(FieldInfo(annotation=str), "abcdef")

import pytest
from pydantic.fields import Undefined

from param import resolvers
from param.errors import ResolutionError
from param.parameters import Param


def test_resolve_param_default_has_argument() -> None:
    assert (
        resolvers.resolve_field_info(
            param=Param(
                alias="foo",
                default=123,
            ),
            argument=456,
        )
        == 456
    )


def test_resolve_param_default_no_argument() -> None:
    assert (
        resolvers.resolve_field_info(
            param=Param(
                alias="foo",
                default=123,
            ),
            argument=Undefined,
        )
        == 123
    )


def test_resolve_param_default_factory_has_argument() -> None:
    assert (
        resolvers.resolve_field_info(
            param=Param(
                alias="foo",
                default_factory=lambda: 123,
            ),
            argument=456,
        )
        == 456
    )


def test_resolve_param_default_factory_no_argument() -> None:
    assert (
        resolvers.resolve_field_info(
            param=Param(
                alias="foo",
                default_factory=lambda: 123,
            ),
            argument=Undefined,
        )
        == 123
    )


def test_resolve_param_no_default_no_argument() -> None:
    with pytest.raises(ResolutionError):
        resolvers.resolve_field_info(
            param=Param(alias="foo"),
            argument=Undefined,
        )

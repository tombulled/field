from pydantic.fields import Undefined

from param import resolvers
from param.enums import ParameterType
from param.models import Parameter, Resolvable
from param.parameters import Param


def test_resolve_param_has_argument() -> None:
    resolvable: Resolvable = Resolvable(
        parameter=Parameter(
            name="foo",
            default=123,
            annotation=int,
            type=ParameterType.POSITIONAL_ONLY,
        ),
        field=Param(
            default=123,
        ),
        argument=456,
    )

    assert resolvers.resolve_param(resolvable) == 456


def test_resolve_param_has_default() -> None:
    resolvable: Resolvable = Resolvable(
        parameter=Parameter(
            name="foo",
            default=123,
            annotation=int,
            type=ParameterType.POSITIONAL_ONLY,
        ),
        field=Param(
            default=123,
        ),
        argument=Undefined,
    )

    assert resolvers.resolve_param(resolvable) == 123


def test_resolve_param_has_default_factory() -> None:
    resolvable: Resolvable = Resolvable(
        parameter=Parameter(
            name="foo",
            default=Undefined,
            annotation=int,
            type=ParameterType.POSITIONAL_ONLY,
        ),
        field=Param(default_factory=lambda: 123),
        argument=Undefined,
    )

    assert resolvers.resolve_param(resolvable) == 123

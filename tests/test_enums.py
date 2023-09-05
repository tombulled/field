from inspect import _ParameterKind as ParameterKind

from param.enums import ParameterType


def test_ParameterType_init() -> None:
    assert (
        ParameterType(ParameterKind.POSITIONAL_OR_KEYWORD)
        is ParameterType.POSITIONAL_OR_KEYWORD
    )


def test_ParameterType_repr() -> None:
    assert (
        repr(ParameterType.POSITIONAL_OR_KEYWORD)
        == "<ParameterType.POSITIONAL_OR_KEYWORD>"
    )

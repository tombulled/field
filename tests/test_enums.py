from inspect import _ParameterKind as ParameterKind

from param.enums import ParameterType


def test_parameter_type_repr() -> None:
    assert (
        repr(ParameterType.POSITIONAL_OR_KEYWORD)
        == "<ParameterType.POSITIONAL_OR_KEYWORD>"
    )


def test_parameter_from_kind() -> None:
    assert (
        ParameterType.from_kind(ParameterKind.POSITIONAL_OR_KEYWORD)
        is ParameterType.POSITIONAL_OR_KEYWORD
    )

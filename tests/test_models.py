import inspect

from param.enums import ParameterType
from param.models import Parameter


def test_parameter_from_parameter() -> None:
    inspect_parameter: inspect.Parameter = inspect.Parameter(
        name="foo",
        kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
        default=123,
        annotation=int,
    )

    assert Parameter.from_parameter(inspect_parameter) == Parameter(
        name="foo",
        type=ParameterType.POSITIONAL_OR_KEYWORD,
        default=123,
        annotation=int,
    )

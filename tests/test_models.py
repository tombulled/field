import inspect
from param.enums import ParameterType
from param.models import Arguments, BoundArguments, Parameter
from typing import Any


def test_arguments() -> None:
    def captor(*args: Any, **kwargs: Any) -> Arguments:
        return Arguments(args=args, kwargs=kwargs)

    arguments: Arguments = Arguments(args=("foo",), kwargs={"bar": "bar"})

    assert arguments.call(captor) == arguments


def test_bound_arguments() -> None:
    def captor(name: str, age: int = 40) -> dict:
        return dict(name=name, age=age)

    assert BoundArguments(args={"name": "sam"}, kwargs={}).call(captor) == {
        "name": "sam",
        "age": 40,
    }
    assert BoundArguments(args={"name": "john"}, kwargs={"age": 10}).call(captor) == {
        "name": "john",
        "age": 10,
    }


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

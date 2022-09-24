import inspect

from param import manager, parameters
from param.api import get_arguments, get_params
from param.enums import ParameterType
from param.models import Arguments, BoundArguments, Parameter
from param.sentinels import Missing
from param.wrappers import Param


def test_parse_empty() -> None:
    assert manager._parse(inspect.Parameter.empty) is Missing


def test_parse_not_empty() -> None:
    assert manager._parse(123) == 123


def test_get_params() -> None:
    def func(a: int, b: str = "b", **c: bool) -> None:
        ...

    assert get_params(func) == {
        "a": Parameter(
            name="a",
            default=parameters.Param(),
            annotation=int,
            type=ParameterType.POSITIONAL_OR_KEYWORD,
        ),
        "b": Parameter(
            name="b",
            default=parameters.Param(default="b"),
            annotation=str,
            type=ParameterType.POSITIONAL_OR_KEYWORD,
        ),
        "c": Parameter(
            name="c",
            default=parameters.Param(),
            annotation=bool,
            type=ParameterType.VAR_KEYWORD,
        ),
    }


def test_get_arguments() -> None:
    def func(a: int, b: str = "b", c: bool = Param(default=True)) -> None:
        ...

    assert get_arguments(func, Arguments(args=(123,))) == BoundArguments(
        args={"a": 123, "b": "b", "c": True}, kwargs={}
    )


def test_get_bound_arguments() -> None:
    def func(a: int, b: str = "b", c: bool = Param(default=True)) -> None:
        ...

    assert manager._bind_arguments(func, Arguments(args=(123,))) == BoundArguments(
        args={"a": 123, "b": "b", "c": Param(default=True)},
        kwargs={},
    )

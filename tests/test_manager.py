import inspect

from param import decorators, manager, parameters
from param.enums import ParameterType
from param.models import Arguments, BoundArguments, Parameter
from param.sentinels import Missing
from param.wrappers import Param


def test_parse_empty() -> None:
    assert manager._parse(inspect._empty) is Missing


def test_parse_not_empty() -> None:
    assert manager._parse(123) == 123


def test_get_params() -> None:
    def func(a: int, b: str = "b", **c: bool) -> None:
        ...

    assert decorators.MANAGER.get_params(func) == {
        "a": Parameter(
            name="a",
            annotation=int,
            type=ParameterType.POSITIONAL_OR_KEYWORD,
            spec=parameters.Param(),
        ),
        "b": Parameter(
            name="b",
            annotation=str,
            type=ParameterType.POSITIONAL_OR_KEYWORD,
            spec=parameters.Param(default="b"),
        ),
        "c": Parameter(
            name="c",
            annotation=bool,
            type=ParameterType.VAR_KEYWORD,
            spec=parameters.Param(),
        ),
    }


def test_get_arguments() -> None:
    def func(a: int, b: str = "b", c: bool = Param(default=True)) -> None:
        ...

    assert decorators.MANAGER.get_arguments(
        func, Arguments(args=(123,))
    ) == BoundArguments(args={"a": 123, "b": "b", "c": True}, kwargs={})


def test_get_bound_arguments() -> None:
    def func(a: int, b: str = "b", c: bool = Param(default=True)) -> None:
        ...

    assert manager._get_bound_arguments(func, Arguments(args=(123,))) == BoundArguments(
        args={"a": 123, "b": "b", "c": Param(default=True)},
        kwargs={},
    )

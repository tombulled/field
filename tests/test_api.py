from param import api
import inspect
from param import parameters
from param.sentinels import Missing
from param.models import Arguments, Parameter
from param.enums import ParameterType
from param.wrappers import Param


def test_parse_empty() -> None:
    assert api._parse(inspect._empty) is Missing


def test_parse_not_empty() -> None:
    assert api._parse(123) == 123


def test_get_params() -> None:
    def func(a: int, b: str = "b", **c: bool) -> None:
        ...

    assert api.get_params(func) == {
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

    assert api.get_arguments(func, (123,), {}) == Arguments(
        args=(123, "b", True), kwargs={}, arguments={"a": 123, "b": "b", "c": True}
    )


def test_get_bound_arguments() -> None:
    def func(a: int, b: str = "b", c: bool = Param(default=True)) -> None:
        ...

    assert api._get_bound_arguments(func, (123,), {}) == (
        {"a": 123, "b": "b", "c": Param(default=True)},
        {},
    )

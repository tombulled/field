from param import api
import inspect
from param.sentinels import Missing
from param.models import Parameter
from param.enums import ParameterKind
from param.param import Param


def test_parse_empty() -> None:
    assert api.parse(inspect._empty) is Missing


def test_parse_not_empty() -> None:
    assert api.parse(123) == 123


def test_get_params() -> None:
    def func(a: int, b: str = "b", **c: bool) -> None:
        ...

    assert api.get_params(func) == {
        "a": Parameter(
            name="a",
            annotation=int,
            kind=ParameterKind.POSITIONAL_OR_KEYWORD,
            spec=Param(),
        ),
        "b": Parameter(
            name="b",
            annotation=str,
            kind=ParameterKind.POSITIONAL_OR_KEYWORD,
            spec=Param(default="b")
        ),
        "c": Parameter(
            name="c", annotation=bool, kind=ParameterKind.VAR_KEYWORD, spec=Param()
        ),
    }

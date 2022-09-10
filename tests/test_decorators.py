from typing import Callable

from param import Param, params
from pytest import fixture


@fixture
def say() -> Callable:
    @params
    def say(message: str = Param(default="Hello, World!")) -> str:
        return message

    return say


def test_params_default(say: Callable):
    assert say() == "Hello, World!"


def test_params_not_default(say: Callable):
    assert say("Hello, Aliens!") == "Hello, Aliens!"

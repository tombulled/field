from param.models import Arguments, BoundArguments
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

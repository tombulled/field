from param.validation import validate

from typing import Any, Dict


def test_validate_all_no_defaults() -> None:
    @validate
    def func_1(x: int, /, y: str, *args: Any, z: int, **kwargs: Any) -> Dict[str, Any]:
        return dict(x=x, y=y, args=args, z=z, kwargs=kwargs)

    assert func_1(123, "abc", "cat", "dog", z=456, name="sam") == {
        "x": 123,
        "y": "abc",
        "args": ("cat", "dog"),
        "z": 456,
        "kwargs": {"name": "sam"},
    }


def test_validate_pos_or_kw_no_defaults() -> None:
    @validate
    def func_2(a: int, b: str) -> Dict[str, Any]:
        return dict(a=a, b=b)

    assert func_2(1, "foo") == {"a": 1, "b": "foo"}
    assert func_2("123", 456) == {"a": 123, "b": "456"}  #  type: ignore

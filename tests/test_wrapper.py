import pytest
from param import wrapper, param


def test_wrapper_default() -> None:
    assert wrapper.Param(default=123) == param.Param(default=123)


def test_wrapper_default_factory() -> None:
    assert wrapper.Param(default_factory=dict) == param.Param(default_factory=dict)


def test_wrapper_default_and_default_factory() -> None:
    with pytest.raises(ValueError):
        wrapper.Param(default=123, default_factory=dict)

import pytest
from param import parameters, wrappers


def test_wrapper_no_default() -> None:
    assert wrappers.Param() == parameters.Param()


def test_wrapper_default() -> None:
    assert wrappers.Param(default=123) == parameters.Param(default=123)


def test_wrapper_default_factory() -> None:
    assert wrappers.Param(default_factory=dict) == parameters.Param(
        default_factory=dict
    )


def test_wrapper_default_and_default_factory() -> None:
    with pytest.raises(ValueError):
        wrappers.Param(default=123, default_factory=lambda: 123)

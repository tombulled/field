import pytest
from param import models, wrappers


def test_wrapper_no_default() -> None:
    assert wrappers.Param() == models.Param()


def test_wrapper_default() -> None:
    assert wrappers.Param(default=123) == models.Param(default=123)


def test_wrapper_default_factory() -> None:
    assert wrappers.Param(default_factory=dict) == models.Param(default_factory=dict)


def test_wrapper_default_and_default_factory() -> None:
    with pytest.raises(ValueError):
        wrappers.Param(default=123, default_factory=lambda: 123)

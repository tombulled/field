import pytest
from param import Param, ParameterSpecification


def test_wrapper_default() -> None:
    assert Param(default=123) == ParameterSpecification(default=123)


def test_wrapper_default_factory() -> None:
    assert Param(default_factory=dict) == ParameterSpecification(default_factory=dict)


def test_wrapper_default_and_default_factory() -> None:
    with pytest.raises(ValueError):
        Param(default=123, default_factory=dict)

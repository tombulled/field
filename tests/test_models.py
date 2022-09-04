import pytest
from param import Missing
from param.models import Param


def test_param_spec_no_default() -> None:
    assert Param().get_default() is Missing


def test_param_spec_default() -> None:
    assert Param(default=123).get_default() == 123


def test_param_spec_default_factory() -> None:
    assert Param(default_factory=dict).get_default() == {}


def test_param_spec_default_and_default_factory() -> None:
    with pytest.raises(ValueError):
        Param(default=123, default_factory=lambda: 123)

from param.parameters import Param

from pydantic.fields import Undefined


def test_no_default() -> None:
    param: Param = Param()

    assert not param.has_default()
    assert param.get_default() is Undefined


def test_default() -> None:
    param: Param = Param(default=123)

    assert param.has_default()
    assert param.get_default() == 123


def test_default_factory() -> None:
    param: Param = Param(default_factory=dict)

    assert param.has_default()
    assert param.get_default() == {}

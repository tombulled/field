from inspect import Parameter

from pydantic.fields import Undefined

from param import utils


def test_parse():
    assert utils.parse(Parameter.empty) is Undefined
    assert utils.parse(123) == 123

from inspect import Parameter

from param import utils
from param.sentinels import Undefined


def test_parse():
    assert utils.parse(Parameter.empty) is Undefined
    assert utils.parse(123) == 123

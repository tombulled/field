from inspect import Parameter

from param import utils
from param.sentinels import Undefined


def test_parse():
    assert utils.empty_to_missing(Parameter.empty) is Undefined
    assert utils.empty_to_missing(123) == 123

from inspect import Parameter

from param import utils
from param.sentinels import Undefined


def test_parse():
    assert utils.parse_parameter_value(Parameter.empty) is Undefined
    assert utils.parse_parameter_value(123) == 123

from param import utils
from param.sentinels import Missing
from inspect import Parameter


def test_parse():
    assert utils.parse(Parameter.empty) is Missing
    assert utils.parse(123) == 123

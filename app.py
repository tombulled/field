import inspect

from param import Param, params
from param.api import get_params


def process_1(data: dict = {}):
    print(id(data))


# @params
# def process_2(data: dict = Param(default_factory=dict)):
#     print(id(data))

# process_1()
# process_1()

# process_2()
# process_2()

# ba = inspect.signature(process_2).bind(process_2)
# a = ba.arguments

def func(a: int, b: str = "b", **c: bool) -> None:
    ...

d = get_params(func)

p = dict(inspect.signature(func).parameters)

# i = p["bar"]
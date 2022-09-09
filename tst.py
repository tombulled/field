from param import Param, params

@params
def foo(bar: str = Param(default="default")):
    return bar

d = foo()
d2 = foo("bar")
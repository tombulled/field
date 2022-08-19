import param


@param.params
def func(a: int, b: str = "b", c: bool = param.Param(default=False), **d: bool) -> None:
    ...


p = param.get_params(func)
a = param.get_arguments(func, (123,), {})

import param


def func(a: int, b: str = "b", **c: bool) -> None:
    ...


d = param.get_params(func)
import param
import param.api


@param.params
def func(
    a: int = param.Param(),
    b: str = "b",
    c: bool = param.Param(default=False),
    **d: bool
) -> dict:
    return dict(a=a, b=b, c=c, d=d)


p = param.get_params(func)
# a = param.get_arguments(func, (123,), {})

# ba = param.api.get_bound_arguments(func, (123,), {})

d = func(123)

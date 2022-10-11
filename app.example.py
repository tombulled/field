from param import Param, params


@params
def get(
    url: str,
    params: dict = Param(default_factory=dict),
):
    print("GET", url, params)


d = get("https://httpbin.com/get")

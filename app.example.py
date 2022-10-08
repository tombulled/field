from param import Param, params

@params
def get(url: str, params: dict = Param(default_factory=dict), name: str = Param(max_length=10)):
    print("GET", url, params, name)

d = get("https://httpbin.com/get")
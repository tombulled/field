from param import Param, params

@params
def get(url: str, params: dict = Param(default_factory=dict)):
    print("GET", url, params)

class MyClass:
    @params
    def get(self, url: str, params: dict = Param(default_factory=dict)):
        print("GET", url, params)

get("https://httpbin.com/get")
MyClass().get("https://httpbin.com/get")
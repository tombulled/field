from param import Param, params, get_params
from abc import ABC

@params
def get(url: str, params: dict = Param(default_factory=dict)):
    print("GET", url, params)

class MyClass(ABC):
    @params
    def get(self, url: str, params: dict = Param(default_factory=dict)):
        print("GET", url, params)

get("https://httpbin.com/get")
MyClass.get("self here", "https://httpbin.com/get")
MyClass().get("https://httpbin.com/get")
from param import Param, params, get_params
from abc import ABC

@params
def get(url: str, params: dict = Param(default_factory=dict)):
    print("GET", url, params)

class MyClass(ABC):
    @params
    def get1(self, url: str, params: dict = Param(default_factory=dict)):
        print("GET", url, params)

    @params
    @classmethod
    def get2(cls, url: str, params: dict = Param(default_factory=dict)):
        print("GET", url, params)

    @params
    @staticmethod
    def get3(url: str, params: dict = Param(default_factory=dict)):
        print("GET", url, params)

get("https://httpbin.com/get")
MyClass().get1("https://httpbin.com/get")
MyClass().get2("https://httpbin.com/get")
MyClass.get2("https://httpbin.com/get")
MyClass().get3("https://httpbin.com/get")
MyClass.get3("https://httpbin.com/get")
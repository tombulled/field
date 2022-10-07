from param import Param, params
from abc import ABC


@params
def get(url: str, params: dict = Param(default_factory=dict)):
    print("GET", url, params)


class MyClass(ABC):
    @params
    def get1(self, url: str, params: dict = Param(default_factory=dict)):
        print("GET", url, params)

    @classmethod
    @params
    def get2(cls, url: str, params: dict = Param(default_factory=dict)):
        print("GET", url, params)

    @staticmethod
    @params
    def get3(url: str, params: dict = Param(default_factory=dict)):
        print("GET", url, params)


get("https://httpbin.com/get")
MyClass().get1("https://httpbin.com/get")
MyClass().get2("https://httpbin.com/get")
MyClass.get2("https://httpbin.com/get")
MyClass().get3("https://httpbin.com/get")
MyClass.get3("https://httpbin.com/get")

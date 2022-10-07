from param import Param, params


@params
def get(url: str, params: dict = Param(default_factory=dict)):
    print("GET", url, params)


class MyClass:
    @params
    def get(self, url: str, params: dict = Param(default_factory=dict)):
        print("GET", url, params)

    @classmethod
    @params
    def post(cls, url: str, params: dict = Param(default_factory=dict)):
        print("POST", url, params)

    @staticmethod
    @params
    def put(url: str, params: dict = Param(default_factory=dict)):
        print("PUT", url, params)


get("https://httpbin.com/get")
MyClass().get("https://httpbin.com/get")
MyClass().post("https://httpbin.com/get")
MyClass.post("https://httpbin.com/get")
MyClass().put("https://httpbin.com/get")
MyClass.put("https://httpbin.com/get")

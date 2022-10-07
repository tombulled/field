# param
Enhanced function parameters

## Installation
```console
pip install git+https://github.com/tombulled/param.git@main
```

## Usage
### Functions
The `@params` annotation works seamlessly with functions:
```python
from param import Param, params

@params
def get(url: str, params: dict = Param(default_factory=dict)):
    print("GET", url, params)
```
```python
>>> get("https://httpbin.com/get")
GET https://httpbin.com/get {}
```

### Classes
The `@params` annotation also works seamlessly with classes. Importantly, the `@params` annotation should be specified before `@staticmethod` or `@classmethod`.
```python
from param import Param, params

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
```
```python
>>> obj = MyClass()
>>>
>>> obj.get("https://httpbin.com/get")
GET https://httpbin.com/get {}
>>>
>>> obj.post("https://httpbin.com/post")
POST https://httpbin.com/post {}
>>> MyClass.post("https://httpbin.com/post")
POST https://httpbin.com/post {}
>>>
>>> obj.put("https://httpbin.com/put")
PUT https://httpbin.com/put {}
>>> MyClass.put("https://httpbin.com/put")
PUT https://httpbin.com/put {}
```
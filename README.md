# param
Enhanced function parameters

## Installation
```console
pip install git+https://github.com/tombulled/param.git@main
```

## Usage
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
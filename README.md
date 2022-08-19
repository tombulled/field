# param
Enhanced function parameters

## Installation
```sh
pip install git+https://github.com/tombulled/param.git@main
```

## Usage
```python
from param import Param, params

@params
def say(message: str = Param(default="Hello, World!")):
    print(message)
```
```python
>>> say("Hello, Bob!")
Hello, Bob!
```
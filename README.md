# param
Enhanced function parameters

## Installation
### PyPI
```console
pip install tombulled-param
```
### GitHub
```console
pip install git+https://github.com/tombulled/param.git@main
```

## Usage
### 1. Create `Params` Instance
```python
from param import Params

params = Params()
```

### 2. Create a Metadata Class
```python
from dataclasses import dataclass

@dataclass
class Punctuate:
    punctation: str
```

### 3. Create a Resolver for the Metadata
```python
from typing import Any

@params.resolver(Punctuate)
def resolve_punctuate(metadata: Punctuate, argument: Any) -> str:
    if not isinstance(argument, str):
        raise TypeError(f"Cannot punctuate argument of type {type(argument)!r}")

    return argument + metadata.punctation
```

### 4. Create a Callable
```python
@params
def greet(name: Annotated[str, Punctuate("!")], /) -> str:
    return f"Hello, {name}"
```

#### 5. Invoke the Callable
```python
>>> greet("Bob")
"Hello, Bob!"
```
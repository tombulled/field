# meta
Parameter Metadata Management

## Installation
### PyPI
```console
pip install ...
```
### GitHub
```console
pip install ...
```

## Usage
### 1. Create a `Meta` Instance
```python
from meta import Meta

meta = Meta()
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
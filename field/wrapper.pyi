from typing import Any, Callable, TypeVar, overload

T = TypeVar("T")

@overload
def Field() -> Any: ...
@overload
def Field(*, default: T) -> T: ...
@overload
def Field(*, default_factory: Callable[[], T]) -> T: ...

from typing import Any, Callable, TypeVar, overload

T = TypeVar("T")

@overload
def Param() -> Any: ...
@overload
def Param(*, default: T) -> T: ...
@overload
def Param(*, default_factory: Callable[[], T]) -> T: ...

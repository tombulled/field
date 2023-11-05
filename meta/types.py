from typing import Protocol, TypeVar, runtime_checkable

__all__ = ("SupportsGt",)

T = TypeVar("T")


@runtime_checkable
class SupportsGt(Protocol):
    def __gt__(self: T, __other: T) -> bool:
        ...

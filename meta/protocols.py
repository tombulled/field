from typing import Protocol, TypeVar, runtime_checkable

__all__ = ("SupportsGt", "SupportsGe", "SupportsLt")

T = TypeVar("T")


@runtime_checkable
class SupportsGt(Protocol):
    def __gt__(self: T, __other: T) -> bool:
        ...


@runtime_checkable
class SupportsGe(Protocol):
    def __ge__(self: T, __other: T) -> bool:
        ...


@runtime_checkable
class SupportsLt(Protocol):
    def __lt__(self: T, __other: T) -> bool:
        ...

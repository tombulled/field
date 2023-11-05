from typing import Protocol, TypeVar, runtime_checkable

__all__ = (
    "SupportsGt",
    "SupportsGe",
    "SupportsLt",
    "SupportsLe",
    "SupportsMod",
    "SupportsDiv",
)

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


@runtime_checkable
class SupportsLe(Protocol):
    def __le__(self: T, __other: T) -> bool:
        ...


@runtime_checkable
class SupportsMod(Protocol):
    def __mod__(self: T, __other: T) -> T:
        ...


@runtime_checkable
class SupportsDiv(Protocol):
    def __div__(self: T, __other: T) -> T:
        ...

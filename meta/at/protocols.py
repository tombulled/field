from typing import Protocol, runtime_checkable

import annotated_types as at

__all__ = (
    "SupportsGt",
    "SupportsGe",
    "SupportsLt",
    "SupportsLe",
    "SupportsMod",
    "SupportsDiv",
)


@runtime_checkable
class SupportsGt(at.SupportsGt, Protocol):
    ...


@runtime_checkable
class SupportsGe(at.SupportsGe, Protocol):
    ...


@runtime_checkable
class SupportsLt(at.SupportsLt, Protocol):
    ...


@runtime_checkable
class SupportsLe(at.SupportsLe, Protocol):
    ...


@runtime_checkable
class SupportsMod(at.SupportsMod, Protocol):
    ...


@runtime_checkable
class SupportsDiv(at.SupportsDiv, Protocol):
    ...

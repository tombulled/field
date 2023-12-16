from typing import Sized

from .protocols import SupportsGe, SupportsGt, SupportsLe, SupportsLt, SupportsMod

__all__ = (
    "gt",
    "lt",
    "ge",
    "le",
    "multiple_of",
    "min_len",
    "max_len",
)


def gt(a: SupportsGt, b: SupportsGt) -> bool:
    """True if `a` is greater than `b`"""

    return a > b


def lt(a: SupportsLt, b: SupportsLt) -> bool:
    """True if `a` is less than `b`"""

    return a < b


def ge(a: SupportsGe, b: SupportsGe) -> bool:
    """True if `a` is greater than or equal to `b`"""

    return a >= b


def le(a: SupportsLe, b: SupportsLe) -> bool:
    """True if `a` is less than or equal to `b`"""

    return a <= b


def multiple_of(a: SupportsMod, b: int) -> bool:
    """True if `a` is a multiple of `b`"""

    return bool(a % b == 0)


def min_len(a: Sized, b: int) -> bool:
    return len(a) >= b


def max_len(a: Sized, b: int) -> bool:
    return len(a) <= b

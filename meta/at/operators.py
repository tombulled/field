from typing import Any, Sized

from .protocols import (
    SupportsDiv,
    SupportsGe,
    SupportsGt,
    SupportsLe,
    SupportsLt,
    SupportsMod,
)

__all__ = (
    "gt",
    "lt",
    "ge",
    "le",
    "multiple_of_mod",
    "multiple_of_div",
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


def multiple_of_mod(a: SupportsMod, b: Any) -> bool:
    """True if `a` is a multiple of `b`"""

    return a % b == 0

def multiple_of_div(a: SupportsDiv, b: Any) -> bool:
    """True if `a` is a multiple of `b`"""

    return int(a / b) == a / b


def min_len(a: Sized, b: int) -> bool:
    return len(a) >= b


def max_len(a: Sized, b: int) -> bool:
    return len(a) <= b

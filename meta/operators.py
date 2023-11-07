from typing import Any, Sized
from .protocols import (
    SupportsGe,
    SupportsGt,
    SupportsLe,
    SupportsLt,
    SupportsMod,
)


# NOTE: Should `b` be typed as `SupportsComparison` instead?
def gt(a: SupportsGt, b: SupportsGt) -> bool:
    return bool(a > b)


def lt(a: SupportsLt, b: SupportsLt) -> bool:
    return bool(a < b)


def ge(a: SupportsGe, b: SupportsGe) -> bool:
    return bool(a >= b)


def le(a: SupportsLe, b: SupportsLe) -> bool:
    return bool(a <= b)


def multiple_of(a: SupportsMod, b: int) -> bool:
    """True if `a` is a multiple of `b`"""

    return bool(a % b == 0)


def min_len(a: Sized, b: int) -> bool:
    return len(a) >= b


def max_len(constraint: MaxLen, value: Any) -> bool:
    assert isinstance(value, Sized)

    return len(value) <= constraint.max_length


def predicate(predicate, value: Any) -> bool:
    return predicate(value)

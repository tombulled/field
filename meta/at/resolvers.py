from datetime import datetime, timezone
from typing import Any, Sized

from annotated_types import (
    Ge,
    Gt,
    Le,
    Lt,
    MaxLen,
    MinLen,
    MultipleOf,
    Predicate,
    Timezone,
)

from .protocols import SupportsGe, SupportsGt, SupportsLe, SupportsLt, SupportsMod

__all__ = (
    "check_gt",
    "check_ge",
    "check_lt",
    "check_le",
    "check_multiple_of",
    "check_min_len",
    "check_max_len",
    "check_timezone",
    "check_predicate",
)


def _assert_isinstance(obj: Any, *types: type) -> None:
    if not isinstance(obj, types):
        raise TypeError(f"Expected value of type {types}, got {type(obj)}")


def check_gt(constraint: Gt, value: Any) -> bool:
    _assert_isinstance(value, SupportsGt)

    return value > constraint.gt


def check_lt(constraint: Lt, value: Any) -> bool:
    _assert_isinstance(value, SupportsLt)

    return value < constraint.lt


def check_ge(constraint: Ge, value: Any) -> bool:
    _assert_isinstance(value, SupportsGe)

    return value >= constraint.ge


def check_le(constraint: Le, value: Any) -> bool:
    _assert_isinstance(value, SupportsLe)

    return value <= constraint.le


def check_multiple_of(constraint: MultipleOf, value: Any) -> bool:
    _assert_isinstance(value, SupportsMod)

    return value % constraint.multiple_of == 0


def check_min_len(constraint: MinLen, value: Any) -> bool:
    _assert_isinstance(value, Sized)

    return len(value) >= constraint.min_length


def check_max_len(constraint: MaxLen, value: Any) -> bool:
    _assert_isinstance(value, Sized)

    return len(value) <= constraint.max_length


def check_predicate(constraint: Predicate, value: Any) -> bool:
    return constraint.func(value)


def check_timezone(constraint: Timezone, value: Any) -> bool:
    _assert_isinstance(value, datetime)

    has_tz: bool = value.tzinfo is not None

    if constraint.tz is None:
        return not has_tz
    elif constraint.tz is Ellipsis:
        return has_tz
    elif isinstance(constraint.tz, str):
        return has_tz and constraint.tz == value.tzname()
    elif isinstance(constraint.tz, timezone):
        return has_tz and value.tzinfo == constraint.tz

    raise TypeError

import sys
from datetime import datetime, timezone
from typing import Any, Sized, TypeVar

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

from . import operators
from .protocols import (
    SupportsDiv,
    SupportsGe,
    SupportsGt,
    SupportsLe,
    SupportsLt,
    SupportsMod,
)

__all__ = (
    "resolve_gt",
    "resolve_ge",
    "resolve_lt",
    "resolve_le",
    "resolve_multiple_of",
    "resolve_min_len",
    "resolve_max_len",
    "resolve_timezone",
    "resolve_predicate",
)

T = TypeVar("T")


def _assert_isinstance(obj: Any, *types: type) -> None:
    if not isinstance(obj, types):
        raise TypeError(f"Expected value of type {types}, got {type(obj)}")


def resolve_gt(constraint: Gt, value: Any) -> bool:
    _assert_isinstance(value, SupportsGt)

    return operators.gt(value, constraint.gt)


def resolve_lt(constraint: Lt, value: Any) -> bool:
    _assert_isinstance(value, SupportsLt)

    return operators.lt(value, constraint.lt)


def resolve_ge(constraint: Ge, value: Any) -> bool:
    _assert_isinstance(value, SupportsGe)

    return operators.ge(value, constraint.ge)


def resolve_le(constraint: Le, value: Any) -> bool:
    _assert_isinstance(value, SupportsLe)

    return operators.le(value, constraint.le)

def resolve_multiple_of(constraint: MultipleOf, value: Any) -> bool:
    # _check_instance(value, SupportsMod)
    # _assert_isinstance(value, SupportsMod)

    return operators.multiple_of(value, constraint.multiple_of)


def resolve_min_len(constraint: MinLen, value: Any) -> bool:
    _assert_isinstance(value, Sized)

    return len(value) >= constraint.min_length


def resolve_max_len(constraint: MaxLen, value: Any) -> bool:
    _assert_isinstance(value, Sized)

    return len(value) <= constraint.max_length


def resolve_predicate(constraint: Predicate, value: Any) -> bool:
    return constraint.func(value)


def resolve_timezone(constraint: Timezone, value: Any) -> bool:
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

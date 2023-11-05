import sys
from datetime import datetime, timezone
from typing import Any, Callable, Sized, TypeVar, Union

import dateutil.tz
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

from .protocols import (
    SupportsDiv,
    SupportsGe,
    SupportsGt,
    SupportsLe,
    SupportsLt,
    SupportsMod,
)

if sys.version_info < (3, 10):
    EllipsisType = type(Ellipsis)
else:
    from types import EllipsisType

T = TypeVar("T")


def resolve_gt(meta: Gt, value: Any) -> SupportsGt:
    gt: SupportsGt = meta.gt

    if not isinstance(value, SupportsGt):
        raise TypeError(
            f"The {Gt.__name__!r} constraint cannot be applied to {type(value)}"
        )

    if not value > gt:
        raise ValueError(f"Value {value} not greater than {gt}")

    return value


def resolve_ge(meta: Ge, value: Any) -> SupportsGe:
    ge: SupportsGe = meta.ge

    if not isinstance(value, SupportsGe):
        raise TypeError(
            f"The {Ge.__name__!r} constraint cannot be applied to {type(value)}"
        )

    if not value >= ge:
        raise ValueError(f"Value {value} not greater than or equal to {ge}")

    return value


def resolve_lt(meta: Lt, value: Any) -> SupportsLt:
    lt: SupportsLt = meta.lt

    if not isinstance(value, SupportsLt):
        raise TypeError(
            f"The {Lt.__name__!r} constraint cannot be applied to {type(value)}"
        )

    if not value < lt:
        raise ValueError(f"Value {value} not less than {lt}")

    return value


def resolve_le(meta: Le, value: Any) -> SupportsLe:
    le: SupportsLe = meta.le

    if not isinstance(value, SupportsLe):
        raise TypeError(
            f"The {Le.__name__!r} constraint cannot be applied to {type(value)}"
        )

    if not value <= le:
        raise ValueError(f"Value {value} not less than or equal to {le}")

    return value


def resolve_multiple_of(meta: MultipleOf, value: T) -> T:
    if isinstance(meta.multiple_of, SupportsMod):
        if not isinstance(value, SupportsMod):
            raise TypeError(f"Operator 'mod' cannot be applied to type {type(value)}")

        if not (value % meta.multiple_of == 0):
            raise ValueError(f"Input should be a multiple of {meta.multiple_of}")

        return value
    elif isinstance(meta.multiple_of, SupportsDiv):
        if not isinstance(value, SupportsDiv):
            raise TypeError(f"Operator 'div' cannot be applied to type {type(value)}")

        if not int(value / meta.multiple_of) == value / meta.multiple_of:
            raise ValueError(f"Input should be a multiple of {meta.multiple_of}")

        return value
    else:
        raise TypeError(f"Invalid `multiple_of` {type(value)}")


def resolve_min_len(meta: MinLen, value: Any) -> Sized:
    min_length: int = meta.min_length

    if not isinstance(value, Sized):
        raise TypeError(
            f"The {MinLen.__name__!r} constraint cannot be applied to {type(value)}"
        )

    if not len(value) >= min_length:
        raise ValueError(f"Value length {len(value)} less than {min_length}")

    return value


def resolve_max_len(meta: MaxLen, value: Any) -> Sized:
    max_length: int = meta.max_length

    if not isinstance(value, Sized):
        raise TypeError(
            f"The {MaxLen.__name__!r} constraint cannot be applied to {type(value)}"
        )

    if not len(value) <= max_length:
        raise ValueError(f"Value length {len(value)} greater than {max_length}")

    return value


def resolve_timezone(meta: Timezone, value: T) -> T:
    tz: Union[str, timezone, EllipsisType, None] = meta.tz

    # TODO: Support usage of `time` as well
    if not isinstance(value, datetime):
        raise TypeError(
            f"The {Timezone.__name__!r} constraint cannot be applied to {type(value)}"
        )

    if tz is None:
        assert value.tzinfo is None

        return value
    elif tz is Ellipsis:
        assert value.tzinfo is not None

        return value
    elif isinstance(tz, timezone):
        raise NotImplementedError # TODO: Implement Me!
    elif isinstance(tz, str):
        print(dateutil.tz.gettz("Europe/Berlin"))
        print(dateutil.tz.gettz(tz))

        raise NotImplementedError # TODO: Implement Me!

    raise NotImplementedError # TODO: Implement Me!


def resolve_predicate(meta: Predicate, value: T) -> T:
    predicate: Callable[[Any], bool] = meta.func

    if not predicate(value):
        raise ValueError(f"Value {value!r} failed predicate {predicate!r}")

    return value

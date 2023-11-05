from typing import Any, Callable, Sized, TypeVar

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
    SupportsGt,
    SupportsGe,
    SupportsLt,
    SupportsLe,
    SupportsMod,
    SupportsDiv,
)

T = TypeVar("T")

# TODO: Rename `resolve` to one of:
#   apply / validate / implement / check / handle / consume / parse?


def resolve_gt(meta: Gt, value: T) -> T:
    gt: SupportsGt = meta.gt

    if not isinstance(value, SupportsGt):
        raise TypeError(f"The {Gt.__name__!r} constraint cannot be applied to {type(value)}")

    if not value > gt:
        # raise ValueError(f"Input should be greater than {gt}")
        # raise ValueError(f"Failed constraint: value > {gt}, where value = {value}")
        # raise ValueError(f"Failed constraint: value > {gt} (value = {value})")
        # raise ValueError(f"Value must be greater than {gt}. Got {value}")
        # raise ValueError(f"Value must be greater than {gt} (got {value})")
        # raise ValueError(f"Value must be greater than {gt} ({value} <= {gt})")
        raise ValueError(f"Value {value} not greater than {gt}")

    return value


def resolve_ge(meta: Ge, value: T) -> T:
    ge: SupportsGe = meta.ge

    if not isinstance(value, SupportsGe):
        raise TypeError(f"The 'ge' constraint cannot be applied to {type(value)}")

    if not value >= ge:
        # raise ValueError(f"Input should be greater than or equal to {ge}")
        # raise ValueError(f"Value {value} not >= {ge}")
        raise ValueError(f"Value {value} not greater than or equal to {ge}")

    return value


def resolve_lt(meta: Lt, value: T) -> T:
    lt: SupportsLt = meta.lt

    if not isinstance(value, SupportsLt):
        raise TypeError(f"The 'lt' constraint cannot be applied to {type(value)}")

    if not value < lt:
        # raise ValueError(f"Input should be less than {lt}")
        raise ValueError(f"Value {value} not less than {lt}")

    return value


def resolve_le(meta: Le, value: T) -> T:
    le: SupportsLe = meta.le

    if not isinstance(value, SupportsLe):
        raise TypeError(f"The 'le' constraint cannot be applied to {type(value)}")

    if not value <= le:
        raise ValueError(f"Input should be less than {le}")

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
        raise TypeError(f"Invalid `multiple_of` value of type {type(value)}")


def resolve_min_len(meta: MinLen, value: T) -> T:
    min_length: int = meta.min_length

    if not isinstance(value, Sized):
        # raise TypeError(f"Input should implement {Sized}")
        raise TypeError(
            f"Function {len.__name__!r} cannot be applied to type {type(value)} (must implement {Sized})"
        )

    if not len(value) >= min_length:
        raise ValueError(f"Length {len(value)} less than {min_length}")

    return value


def resolve_max_len(meta: MaxLen, value: T) -> T:
    max_length: int = meta.max_length

    if not isinstance(value, Sized):
        raise TypeError(f"Input should implement {Sized}")

    if not len(value) <= max_length:
        raise ValueError(f"Length {len(value)} greater than {max_length}")

    return value


def resolve_timezone(meta: Timezone, value: T) -> T:
    raise NotImplementedError


def resolve_predicate(meta: Predicate, value: T) -> T:
    predicate: Callable[[Any], bool] = meta.func
    
    if not predicate(value):
        raise ValueError(f"Value {value!r} failed predicate {predicate!r}")

    return value

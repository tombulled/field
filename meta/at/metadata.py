import dataclasses
from operator import getitem
import sys
from typing import Any

import annotated_types
from annotated_types import DocInfo, Interval, Len, Predicate, Timezone

__all__ = (
    "Gt",
    "Ge",
    "Lt",
    "Le",
    "Interval",
    "MultipleOf",
    "MinLen",
    "MaxLen",
    "Len",
    "Timezone",
    "Predicate",
    "DocInfo",
)


class AnnotatedTypesReprMixin:
    def __repr__(self) -> str:
        value: Any

        if sys.version_info < (3, 10):
            value = next(iter(self.__dict__.values()))
        else:
            value = getattr(self, self.__slots__[0])

        return f"{type(self).__name__}({value})"


class Ge(AnnotatedTypesReprMixin, annotated_types.Ge):
    pass


class Gt(AnnotatedTypesReprMixin, annotated_types.Gt):
    pass


class Le(AnnotatedTypesReprMixin, annotated_types.Le):
    pass


class Lt(AnnotatedTypesReprMixin, annotated_types.Lt):
    pass


class MaxLen(AnnotatedTypesReprMixin, annotated_types.MaxLen):
    pass


class MinLen(AnnotatedTypesReprMixin, annotated_types.MinLen):
    pass


class MultipleOf(AnnotatedTypesReprMixin, annotated_types.MultipleOf):
    pass

from typing import Any, Mapping, Tuple

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
        attrs: Mapping[str, Any] = getattr(self, "__dict__", {})
        slots: Tuple[str, ...] = getattr(self, "__slots__", ())

        value: Any

        if attrs:
            value = next(iter(attrs.values()))
        elif slots:
            value = getattr(self, slots[0])
        else:
            value = ""

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

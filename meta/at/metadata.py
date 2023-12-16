import annotated_types
from annotated_types import DocInfo  # type: ignore [unknown-import]
from annotated_types import (  # Ge,; Gt,; Le,; Lt,; MaxLen,; MinLen,; MultipleOf,
    Interval,
    Len,
    Predicate,
    Timezone,
)

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

# def _build_repr(..., ...):
#     ...


class Ge(annotated_types.Ge):
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.ge})"


class Gt(annotated_types.Gt):
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.gt})"


class Le(annotated_types.Le):
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.le})"


class Lt(annotated_types.Lt):
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.lt})"


class MaxLen(annotated_types.MaxLen):
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.max_length})"


class MinLen(annotated_types.MinLen):
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.min_length})"


class MultipleOf(annotated_types.MultipleOf):
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.multiple_of})"

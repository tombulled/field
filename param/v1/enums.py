from enum import Enum
from inspect import Parameter
from typing import Sequence

__all__: Sequence[str] = ("ParameterType",)


class NoValue(Enum):
    def __repr__(self) -> str:
        return f"<{type(self).__name__}.{self.name}>"


class ParameterType(NoValue):
    POSITIONAL_ONLY = Parameter.POSITIONAL_ONLY
    POSITIONAL_OR_KEYWORD = Parameter.POSITIONAL_OR_KEYWORD
    VAR_POSITIONAL = Parameter.VAR_POSITIONAL
    KEYWORD_ONLY = Parameter.KEYWORD_ONLY
    VAR_KEYWORD = Parameter.VAR_KEYWORD

    @property
    def description(self) -> str:
        return self.value.description

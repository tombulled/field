from enum import Enum, auto
from typing import Literal

from typing_extensions import TypeAlias


class NoValue(Enum):
    def __repr__(self) -> str:
        return f"<{type(self).__name__}.{self.name}>"


class Sentinel(NoValue):
    Missing = auto()


MissingType: TypeAlias = Literal[Sentinel.Missing]

Missing: MissingType = Sentinel.Missing

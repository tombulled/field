from enum import Enum, auto
from typing import Literal, Sequence

from typing_extensions import TypeAlias

__all__: Sequence[str] = ("MissingType", "Missing")


class Sentinel(Enum):
    MISSING = auto()


MissingType: TypeAlias = Literal[Sentinel.MISSING]
Missing: MissingType = Sentinel.MISSING

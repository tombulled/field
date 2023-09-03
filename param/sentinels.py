from enum import auto
from typing import Literal, Sequence

from typing_extensions import TypeAlias

from .enums import NoValue

__all__: Sequence[str] = ("MissingType", "Missing")


class Sentinel(NoValue):
    MISSING = auto()


MissingType: TypeAlias = Literal[Sentinel.MISSING]
Missing: MissingType = Sentinel.MISSING

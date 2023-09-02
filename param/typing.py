from typing import Any, Sequence, TypeVar, Union
from typing_extensions import TypeAlias

from .sentinels import MissingType

__all__: Sequence[str] = ("Argument",)

T = TypeVar("T")

Maybe = Union[T, MissingType]

AnyOrMissing = Maybe[Any]

Argument: TypeAlias = AnyOrMissing

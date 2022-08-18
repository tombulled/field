from dataclasses import dataclass, field
from typing import Any, Dict, Tuple
from .enums import ParameterKind


@dataclass
class Arguments:
    args: Tuple[Any, ...] = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    arguments: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Parameter:
    name: str
    annotation: Any
    kind: ParameterKind
    default: Any

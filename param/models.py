from dataclasses import dataclass, field
from typing import Any, Dict, Tuple
from .enums import ParameterType
from .param import Param


@dataclass
class Arguments:
    args: Tuple[Any, ...] = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    arguments: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Parameter:
    name: str
    annotation: Any
    type: ParameterType
    # default: Any
    spec: Param

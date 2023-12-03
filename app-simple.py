from dataclasses import dataclass
from typing import Any

from typing_extensions import Annotated

from meta import BaseMetadata, Meta, Params


@dataclass(frozen=True)
class Suffix(BaseMetadata):
    suffix: str


def resolve_suffix(meta: Suffix, value: Any) -> str:
    return str(value) + meta.suffix


metas = Meta({Suffix: resolve_suffix})
params = Params(metas)

Name = Annotated[str, Suffix("!")]


@params.wrap
def greet(name: Name) -> str:
    return f"Hello, {name}"

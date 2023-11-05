from dataclasses import dataclass
from typing import Any
from typing_extensions import Annotated
from meta import BaseMetadata, Metas


@dataclass(frozen=True)
class Suffix(BaseMetadata):
    suffix: str


def resolve_suffix(meta: Suffix, value: Any) -> str:
    return meta.suffix + str(value)


metas = Metas({Suffix: resolve_suffix})
params = Params(metas)

Name = Annotated[str, Suffix("!")]

# @meta / @meta.bind / @meta.wrap
@metas
def greet(name: Name) -> str:
    return f"Hello, {name}"

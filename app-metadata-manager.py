from dataclasses import dataclass
from typing import Any

from typing_extensions import Annotated

from meta import BaseMetadata, Meta


@dataclass
class Suffix(BaseMetadata):
    suffix: str


def resolve_suffix(metadata: Suffix, value: Any) -> str:
    assert isinstance(value, str)

    return value + metadata.suffix


meta = Meta({Suffix: resolve_suffix})

assert meta.get_resolver(Suffix) is resolve_suffix
assert meta.get_resolver(str) is None
assert meta.can_resolve(Suffix)
assert not meta.can_resolve(str)
assert meta.resolve("hello") == "hello"
assert meta.resolve("hello", Suffix("!!!")) == "hello!!!"
assert meta.resolve("hello", Suffix("!"), Suffix("?")) == "hello!?"
assert meta.parse(str) == []
assert meta.parse(Annotated[str, Suffix("!")]) == [Suffix("!")]
assert meta.parse(Annotated[str, Suffix("!"), Suffix("?")]) == [
    Suffix("!"),
    Suffix("?"),
]

# Should raise `ResolutionError`
try:
    meta.resolve(123, Suffix("!!!"))
except:
    pass
else:
    assert False

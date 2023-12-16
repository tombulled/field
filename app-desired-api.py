from dataclasses import dataclass
from typing import Any

from meta import Meta


@dataclass
class Punctuate:
    punctation: str

    def apply(self, value: Any) -> str:
        return str(value) + self.punctation


meta = Meta({Punctuate: Punctuate.apply})

assert meta.resolve("hello", Punctuate("!!!")) == "hello!!!"

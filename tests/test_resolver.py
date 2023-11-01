from typing import Any

from param import Resolver


def test_Resolver_isinstance() -> None:
    class Metadata:
        pass

    def my_resolver(metadata: Metadata, argument: Any) -> str:
        return "yo!"

    assert isinstance(my_resolver, Resolver)

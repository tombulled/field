from typing import Protocol, TypeVar

T_co = TypeVar("T_co", covariant=True)


class Supplier(Protocol[T_co]):
    def __call__(self) -> T_co:
        ...

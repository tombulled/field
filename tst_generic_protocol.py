from typing import Protocol, Generic, TypeVar

T = TypeVar("T", covariant=True)

class Producer(Protocol[T]):
    def __call__(self) -> T:
        ...


def int_producer() -> int:
    return 123

ip: Producer = int_producer

d = ip()
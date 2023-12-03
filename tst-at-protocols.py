from typing import Protocol, runtime_checkable
import annotated_types as at

class _SupportsBob(Protocol):
    def bob(self):
        ...

@runtime_checkable
class SupportsBob(_SupportsBob, Protocol):
    pass


class A:
    def bob(self):
        return True


class B:
    pass

a=A()
b=B()
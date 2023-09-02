from typing import Sequence

__all__: Sequence[str] = ("ResolutionError", "MissingSpecification")


class ResolutionError(Exception):
    pass


class MissingSpecification(Exception):
    pass

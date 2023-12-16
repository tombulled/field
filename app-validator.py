from typing import Any, Mapping, Type

from meta import BaseMetadata, Resolver
from meta.at.metadata import Gt

Constraint = BaseMetadata
Validator = Resolver[Constraint, bool]


def validate_gt(constraint: Constraint, value: Any) -> bool:
    assert isinstance(constraint, Gt)

    return value > constraint.gt


VALIDATORS: Mapping[Type[Constraint], Validator] = {
    Gt: validate_gt,
}

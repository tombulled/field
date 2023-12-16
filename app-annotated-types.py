import functools

from meta import resolve
from meta.at.metadata import Gt
from meta.at.resolvers import gt
from meta.at.utils import get_metadata
from meta.typing import Annotated

Gt10 = Gt(10)
BigInt = Annotated[int, Gt10]

gt(Gt10, 100)

gt_10 = functools.partial(gt, Gt(10), "yo")

m = get_metadata(BigInt)

d = resolve(19, Gt10)

# from meta.at import AnnotatedTypesManager
# from meta import AnnotatedTypes
# at = AnnotatedTypes()

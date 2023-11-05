import functools

from meta import resolve
from meta.metadata import Gt
from meta.resolvers import gt
from meta.typing import Annotated
from meta.utils import get_metadata

Gt10 = Gt(10)
BigInt = Annotated[int, Gt10]

gt(Gt10, 100)

gt_10 = functools.partial(gt, Gt(10), "yo")

m = get_metadata(BigInt)

d = resolve(19, Gt10)

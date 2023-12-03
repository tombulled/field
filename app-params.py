from typing_extensions import Annotated

from meta import Meta
from meta.metadata import Gt
from meta.params import Params
from meta.resolvers import gt

metas = Meta({Gt: gt})
params = Params(metas)

AdultAge = Annotated[int, Gt(18)]


@params.wrap
def buy_alcohol(age: AdultAge) -> None:
    print("Buying Alcohol!")


buy_alcohol(12)

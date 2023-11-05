from typing_extensions import Annotated
from meta import Gt, wrap

AdultAge = Annotated[int, Gt(18)]

@wrap
def buy_alcohol(age: AdultAge) -> None:
    print("Buying Alcohol!")

buy_alcohol()

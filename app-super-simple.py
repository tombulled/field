from typing_extensions import Annotated

from meta import Gt, Lt, wrap

ChildAge = Annotated[int, Lt(18)]
AdultAge = Annotated[int, Gt(18)]


@wrap
def buy_alcohol(age: AdultAge) -> None:
    print("Buying Alcohol!")


@wrap
def buy_toy(age: ChildAge) -> None:
    print("Buying Toy!")

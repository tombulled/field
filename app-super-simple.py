from typing_extensions import Annotated

from meta import Ge, Lt, wrap

ChildAge = Annotated[int, Lt(18)]
AdultAge = Annotated[int, Ge(18)]


@wrap
def buy_alcohol(age: AdultAge) -> None:
    print("Buying Alcohol!")


@wrap
def buy_toy(age: ChildAge) -> None:
    print("Buying Toy!")

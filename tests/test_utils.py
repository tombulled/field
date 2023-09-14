from typing_extensions import Annotated

from param import utils


def test_get_metadata() -> None:
    assert utils.get_metadata(str) == ()
    assert utils.get_metadata(Annotated[str, "yo!"]) == ("yo!",)


def test_is_annotated() -> None:
    assert not utils.is_annotated(str)
    assert utils.is_annotated(Annotated[str, "yo!"])


def test_get_annotated_type() -> None:
    assert utils.get_annotated_type(str) == str
    assert utils.get_annotated_type(Annotated[str, "yo!"]) == str

from inspect import Parameter
from typing import Any, Sequence

import pytest
from pydantic_core import PydanticUndefined
from typing_extensions import Annotated

from meta.errors import ResolutionError
from meta.pydantic import ParamInfo, PydanticParams, PydanticResolver


def test_PydanticParams_init() -> None:
    assert PydanticParams().resolvers == {ParamInfo: PydanticResolver()}


def test_PydanticParams_enrich_field_info_infer_alias() -> None:
    param_info: ParamInfo = PydanticParams.enrich_field_info(
        Parameter(
            name="name",
            kind=Parameter.POSITIONAL_OR_KEYWORD,
        ),
        ParamInfo(),
    )

    assert param_info.alias == "name"
    assert param_info.alias_priority == 2


def test_PydanticParams_enrich_field_info_infer_annotation_success() -> None:
    param_info: ParamInfo = PydanticParams.enrich_field_info(
        Parameter(
            name="name",
            kind=Parameter.POSITIONAL_OR_KEYWORD,
            default="Sally",
            annotation=str,
        ),
        ParamInfo(),
    )

    assert param_info.annotation == str


def test_PydanticParams_enrich_field_info_infer_annotation_failure() -> None:
    param_info: ParamInfo = PydanticParams.enrich_field_info(
        Parameter(
            name="name",
            kind=Parameter.POSITIONAL_OR_KEYWORD,
            default="Sally",
        ),
        ParamInfo(),
    )

    assert param_info.annotation == Any


def test_PydanticParams_enrich_field_info_infer_default_success() -> None:
    param_info: ParamInfo = PydanticParams.enrich_field_info(
        Parameter(
            name="name",
            kind=Parameter.POSITIONAL_OR_KEYWORD,
            default="Sally",
        ),
        ParamInfo(),
    )

    assert param_info.default == "Sally"


def test_PydanticParams_enrich_field_info_infer_default_failure() -> None:
    param_info: ParamInfo = PydanticParams.enrich_field_info(
        Parameter(
            name="name",
            kind=Parameter.POSITIONAL_OR_KEYWORD,
        ),
        ParamInfo(),
    )

    assert param_info.default == PydanticUndefined


def test_PydanticParams_get_parameter_metadata() -> None:
    param_info_a: ParamInfo = ParamInfo(alias="a")
    param_info_b: ParamInfo = ParamInfo(alias="b")

    assert (
        PydanticParams().get_parameter_metadata(
            Parameter(
                name="name",
                kind=Parameter.POSITIONAL_OR_KEYWORD,
            )
        )
        == []
    )

    with pytest.raises(ResolutionError):
        PydanticParams().get_parameter_metadata(
            Parameter(
                name="name",
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                annotation=Annotated[str, param_info_a, param_info_b],
            )
        )

    param_infos: Sequence[ParamInfo] = PydanticParams().get_parameter_metadata(
        Parameter(
            name="name",
            kind=Parameter.POSITIONAL_OR_KEYWORD,
            default="Sally",
            annotation=Annotated[str, ParamInfo()],
        )
    )

    assert len(param_infos) == 1

    param_info: ParamInfo = param_infos[0]

    assert param_info.alias == "name"
    assert param_info.default == "Sally"
    assert param_info.annotation == str

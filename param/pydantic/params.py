from inspect import Parameter
from typing import Any, Final, Optional, Sequence

from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from .. import utils
from ..errors import ResolutionError
from ..params import Params
from ..resolver import Resolvers
from .resolver import PydanticResolver

PydanticResolvers = Resolvers[FieldInfo, Any]

DEFAULT_RESOLVERS: Final[PydanticResolvers] = {
    FieldInfo: PydanticResolver(),
}


class PydanticParams(Params[FieldInfo, Any]):
    def __init__(
        self,
        resolvers: Optional[PydanticResolvers] = None,
        /,
    ) -> None:
        self.resolvers = {
            **DEFAULT_RESOLVERS,
            **(resolvers if resolvers is not None else {}),
        }

    @staticmethod
    def enrich_field_info(parameter: Parameter, field_info: FieldInfo) -> FieldInfo:
        if field_info.alias is None:
            field_info.alias = parameter.name
        if (
            field_info.annotation is None
            and parameter.annotation is not Parameter.empty
        ):
            field_info.annotation = utils.get_annotated_type(parameter.annotation)
        if (
            field_info.default is PydanticUndefined
            and parameter.default is not Parameter.empty
        ):
            field_info.default = parameter.default

        return field_info

    def get_parameter_metadata(self, parameter: Parameter, /) -> Sequence[FieldInfo]:
        field_infos: Sequence[FieldInfo] = self.get_metadata(parameter.annotation)

        total_field_infos: int = len(field_infos)

        if total_field_infos == 0:
            return field_infos
        elif len(field_infos) > 1:
            raise ResolutionError(
                f"Expected <=1 metadatas of type {FieldInfo!r}, got {len(field_infos)}"
            )

        # Extract and create a copy of the field metadata
        field_info: FieldInfo = field_infos[0].merge_field_infos()

        # Return an enriched field info
        return [self.enrich_field_info(parameter, field_info)]

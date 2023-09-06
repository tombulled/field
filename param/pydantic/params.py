from typing import Any, Final, Optional, Sequence

from pydantic.fields import FieldInfo

from ..models import Parameter
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

    def get_parameter_metadata(self, parameter: Parameter, /) -> Sequence[FieldInfo]:
        field_infos: Sequence[FieldInfo] = self.get_metadata(parameter.annotation)

        print("Field Infos:", field_infos)

        raise NotImplementedError

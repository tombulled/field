import sys
from dataclasses import dataclass
from typing import Any, Optional

from pydantic import ConfigDict, RootModel
from pydantic.fields import FieldInfo

from ..api import Resolver

if sys.version_info < (3, 9):
    from typing_extensions import Annotated, get_args, get_origin
else:
    from typing import Annotated, get_args, get_origin

__all__ = ("PydanticResolver",)


def get_annotated_type(typ, /):  # TODO: type me
    origin: Optional[Any] = get_origin(typ)

    if origin is not Annotated:
        return typ

    return get_args(typ)[0]


@dataclass
class PydanticResolver(Resolver[FieldInfo, Any]):
    config: Optional[ConfigDict] = None

    def __call__(self, field_info: FieldInfo, value: Any, /) -> Any:
        annotation: Any = (
            field_info.annotation if field_info.annotation is not None else Any
        )

        annotated_type: Any = get_annotated_type(annotation)

        config: ConfigDict = self.config if self.config is not None else ConfigDict()

        class Root(RootModel[annotated_type]):
            model_config = config

            root: annotated_type = field_info

        return Root(root=value).root

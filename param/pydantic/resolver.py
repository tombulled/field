from dataclasses import dataclass
from typing import Any, Optional, Sequence

from pydantic import ConfigDict, RootModel
from pydantic.fields import FieldInfo
from typing_extensions import Annotated

from pydantic_core import PydanticUndefined

from ..resolver import Resolver

__all__: Sequence[str] = ("PydanticResolver",)


@dataclass
class PydanticResolver(Resolver[FieldInfo, Any]):
    config: Optional[ConfigDict] = None

    def __call__(self, field_info: FieldInfo, argument: Any, /) -> Any:
        annotation: Any = (
            field_info.annotation
            if field_info.annotation is not None
            else Any
        )

        if field_info.default is PydanticUndefined:
            field_info = FieldInfo.from_annotation(annotation)
        else:
            field_info = FieldInfo.from_annotated_attribute(
                annotation, field_info.default
            )

        root_model = RootModel[Annotated[annotation, field_info]]

        return root_model(argument).root

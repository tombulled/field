from dataclasses import dataclass
from typing import Any, Optional, Sequence

from pydantic import ConfigDict, RootModel
from pydantic.fields import FieldInfo

from .. import utils
from ..resolver import Resolver

__all__: Sequence[str] = ("PydanticResolver",)


@dataclass
class PydanticResolver(Resolver[FieldInfo, Any]):
    config: Optional[ConfigDict] = None

    def __call__(self, field_info: FieldInfo, argument: Any, /) -> Any:
        annotation: Any = (
            field_info.annotation if field_info.annotation is not None else Any
        )

        annotated_type: Any = utils.get_annotated_type(annotation)

        config: ConfigDict = self.config if self.config is not None else ConfigDict()

        class Root(RootModel[annotated_type]):
            model_config = config

            root: annotated_type = field_info

        return Root(root=argument).root

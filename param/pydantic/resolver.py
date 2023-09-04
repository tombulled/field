from dataclasses import dataclass
from typing import Any, Optional, Sequence

from pydantic import ConfigDict, RootModel
from pydantic.fields import FieldInfo
from typing_extensions import Annotated

from ..models import ResolutionContext
from ..sentinels import Missing
from ..typing import Argument

__all__: Sequence[str] = ("PydanticResolver",)


@dataclass
class PydanticResolver:
    config: Optional[ConfigDict] = None

    def __call__(
        self, context: ResolutionContext[FieldInfo], argument: Argument
    ) -> Any:
        annotation: Any = context.parameter.annotation

        if annotation is Missing:
            annotation = Any

        field_info: FieldInfo

        if context.parameter.default is Missing:
            field_info = FieldInfo.from_annotation(annotation)
        else:
            field_info = FieldInfo.from_annotated_attribute(
                annotation, context.parameter.default
            )

        # WARN: This will end up with 2x FieldInfos in the metadata
        root_model = RootModel[Annotated[annotation, field_info]]

        return root_model(argument).root

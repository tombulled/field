from pydantic import Field, RootModel
from typing_extensions import Annotated

Name = RootModel[Annotated[str, Field(default="sally", max_length=3)]]

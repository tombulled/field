from typing_extensions import Annotated
from pydantic import Field, RootModel

Name = RootModel[Annotated[str, Field(default="sally", max_length=3)]]
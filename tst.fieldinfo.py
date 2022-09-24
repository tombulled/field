from pydantic import BaseConfig, BaseModel, constr
from pydantic.fields import FieldInfo, ModelField, Field
from pydantic.error_wrappers import ValidationError

class MyModel(BaseModel):
    age: int
    name: str = Field(default="sam", max_length=5)

def foo(name: str = Field(default="sam", max_length=5)):
    ...

f = FieldInfo(default="sam", max_length=5)
f._validate()

mf = ModelField(
    name="name",
    type_=constr(max_length=5),
    class_validators={},
    model_config=BaseConfig,
    field_info=f,
    default=f,
    required=False,
    alias=None,
)

v, errors = mf.validate("this is too long", {}, loc=("query", "name"))

if errors:
    raise ValidationError([errors], MyModel)
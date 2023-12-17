from pydantic import ConfigDict
from pydantic.fields import FieldInfo
from meta.pydantic.resolver import PydanticFieldInfoResolver

r = PydanticFieldInfoResolver(
    ConfigDict(str_to_lower=True)
)

# d = r(FieldInfo(annotation=int), "not an int")
d = r(FieldInfo(annotation=str), "SoMe StRiNg")

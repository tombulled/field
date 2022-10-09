from typing import Any
from pydantic.fields import FieldInfo
from pydantic.typing import Annotated


class QueryField(FieldInfo):
    pass


class PathField(FieldInfo):
    pass


def Query(*args, **kwargs) -> Any:
    return QueryField(*args, **kwargs)


def Path(*args, **kwargs) -> Any:
    return PathField(*args, **kwargs)


def get_user(
    user_id: Annotated[int, Path()], details: Annotated[str, Query()] = "full", **kw
) -> list:
    return dict(user_id=user_id, details=details)


from typing import Any, Dict
from pydantic.decorator import ValidatedFunction

validated_function: ValidatedFunction = ValidatedFunction(get_user, None)

values: Dict[str, Any] = validated_function.build_values((123,), {})

from pydantic import BaseModel

model: BaseModel = validated_function.init_model_instance(123)

from functools import wraps


@wraps(get_user)
def wrapper(*args, **kwargs):
    print("Intercepted arguments:", args, kwargs)

    return get_user(*args, **kwargs)


validated_function_for_wrapper: ValidatedFunction = ValidatedFunction(wrapper, None)

_ = validated_function_for_wrapper.call(123)

d = validated_function.call(123)

args: Dict[str, Any] = {
    argument_name: getattr(model, argument_name)
    for argument_name in validated_function.arg_mapping.values()
}

kwargs: Dict[str, Any] = {field_name: ...}

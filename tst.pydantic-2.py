from functools import wraps

from pydantic import Field, Required, validate_arguments
from pydantic.decorator import ValidatedFunction
from pydantic.typing import Annotated


@validate_arguments
def get_user(
    user_id: Annotated[int, Field()], details: Annotated[str, Field()] = "full"
) -> dict:
    return dict(user_id=user_id, details=details)


@wraps(get_user)
def wrapper(*args, **kwargs):
    print("Intercepted arguments:", args, kwargs)

    return get_user(*args, **kwargs)


# validated_function_for_wrapper: ValidatedFunction = ValidatedFunction(get_user, None)

# _ = validated_function_for_wrapper.call(123)
d = get_user(123)
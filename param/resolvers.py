from typing import Any, Callable, Protocol, Type, TypeVar

from pydantic import BaseConfig, Required, BaseModel
from pydantic.fields import ModelField
from pydantic.error_wrappers import ValidationError
from roster import Register

from .models import Resolvable
from .parameters import Param

R = TypeVar("R", bound=Callable)


class Resolver(Protocol):
    def __call__(self, resolvable: Resolvable, /) -> Any:
        ...


class Resolvers(Register[Type[Param], R]):
    pass


RESOLVERS: Resolvers[Resolver] = Resolvers()


@RESOLVERS(Param)
def resolve_param(resolvable: Resolvable[Param], /) -> Any:
    type_: Type[Any]

    if isinstance(resolvable.parameter.annotation, type):
        type_ = resolvable.parameter.annotation
    else:
        raise Exception("Parameter annotation is not a valid type")

    model_field = ModelField(
        name=resolvable.parameter.name,
        type_=type_,
        class_validators={},
        model_config=BaseConfig,
        default=resolvable.field.default,
        default_factory=resolvable.field.default_factory,
        required=resolvable.parameter.default is Required,
        alias=resolvable.field.alias,
        field_info=resolvable.field,
    )

    class FakeModelForTheTimeBeing(BaseModel):
        pass

    value, errors = model_field.validate(
        resolvable.argument, {}, loc=resolvable.parameter.name, cls=FakeModelForTheTimeBeing
    )

    if errors:
        raise ValidationError([errors], FakeModelForTheTimeBeing)

    return value

    # if resolvable.argument is not Missing:
    #     return resolvable.argument
    # elif resolvable.specification.has_default():
    #     return resolvable.specification.get_default()
    # else:
    #     raise ResolutionError("No value provided and parameter has no default")

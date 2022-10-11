from typing import Any, Callable, Protocol, Type, TypeVar

from pydantic import BaseConfig, Required, BaseModel
from pydantic.fields import ModelField, Undefined
from pydantic.error_wrappers import ValidationError
from pydantic.schema import get_annotation_from_field_info
from roster import Register

from .models import Resolvable
from .errors import ResolutionError
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
    return resolvable.argument
    
    # annotation: Any

    # if resolvable.parameter.annotation is Undefined:
    #     annotation = Any
    # else:
    #     annotation = resolvable.parameter.annotation

    # type_: Type[Any] = get_annotation_from_field_info(
    #     annotation=annotation,
    #     field_info=resolvable.field,
    #     field_name=resolvable.parameter.name,
    # )

    # model_field = ModelField(
    #     name=resolvable.parameter.name,
    #     type_=type_,
    #     class_validators=None,
    #     model_config=BaseConfig,
    #     default=resolvable.field.default,
    #     default_factory=resolvable.field.default_factory,
    #     required=resolvable.parameter.default is Required,
    #     alias=resolvable.field.alias,
    #     field_info=resolvable.field,
    # )

    # argument: Any

    # if resolvable.argument is not Undefined:
    #     argument = resolvable.argument
    # elif (
    #     resolvable.field.default is not Undefined
    #     or resolvable.field.default_factory is not None
    # ):
    #     argument = model_field.get_default()
    # else:
    #     raise ResolutionError("No value provided and parameter has no default")

    # value, errors = model_field.validate(
    #     argument, {}, loc=resolvable.parameter.name, cls=BaseModel
    # )

    # if errors:
    #     raise ValidationError([errors], BaseModel)

    # return value

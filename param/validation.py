from functools import wraps
from inspect import Parameter, signature
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Mapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)
from typing_extensions import ParamSpec

from pydantic import Required
from pydantic.config import Extra
from pydantic.main import BaseModel, create_model
from pydantic.typing import get_all_type_hints
from pydantic.utils import to_camel

PS = ParamSpec("PS")
RT = TypeVar("RT")

ConfigType = Union[Type[Any], Dict[str, Any]]


@overload
def validate(
    func: None = None, *, config: Optional[ConfigType] = None
) -> Callable[[Callable[PS, RT]], Callable[PS, RT]]:
    ...


@overload
def validate(func: Callable[PS, RT]) -> Callable[PS, RT]:
    ...


def validate(
    func: Optional[Callable[PS, RT]] = None, *, config: Optional[ConfigType] = None
) -> Union[Callable[PS, RT], Callable[[Callable[PS, RT]], Callable[PS, RT]]]:
    """
    Decorator to validate the arguments passed to a function.
    """

    def decorate(func: Callable[PS, RT], /) -> Callable[PS, RT]:
        validated_func: ValidatedFunction[PS, RT] = ValidatedFunction(
            func, config=config
        )

        @wraps(func)
        def wrapper(*args: PS.args, **kwargs: PS.kwargs) -> RT:
            return validated_func.call(*args, **kwargs)

        setattr(wrapper, "validator", validated_func)

        return wrapper

    if func:
        return decorate(func)
    else:
        return decorate


class ValidatedFunction(Generic[PS, RT]):
    function: Callable[PS, RT]
    parameters: Mapping[str, Parameter]
    model: Type[BaseModel]

    def __init__(
        self, function: Callable[PS, RT], /, *, config: Optional[ConfigType] = None
    ):
        parameters: Mapping[str, Parameter] = signature(function).parameters
        type_hints: Dict[str, Any] = get_all_type_hints(function)
        fields: Dict[str, Tuple[Any, Any]] = {}

        parameter_name: str
        parameter: Parameter
        for parameter_name, parameter in parameters.items():
            annotation: Any

            if parameter.annotation is Parameter.empty:
                annotation = Any
            else:
                annotation = type_hints[parameter_name]

            default: Any

            if parameter.default is Parameter.empty:
                default = Required
            else:
                default = parameter.default

            if parameter.kind == Parameter.VAR_POSITIONAL:
                fields[parameter_name] = (Tuple[annotation, ...], None)
            elif parameter.kind == Parameter.VAR_KEYWORD:
                fields[parameter_name] = (Dict[str, annotation], None)
            else:
                fields[parameter_name] = (annotation, default)

        self.function = function  #  type: ignore
        self.parameters = parameters
        self.model = self._create_model(fields, config=config)

    def _create_model(
        self, fields: Dict[str, Any], *, config: Optional[ConfigType] = None
    ) -> Type[BaseModel]:
        CustomConfig: Type[Any]

        if isinstance(config, dict):
            CustomConfig = type("CustomConfig", (), config)
        elif isinstance(config, type):
            CustomConfig = config
        else:
            CustomConfig = type("CustomConfig", (), {})

        Config: Type[Any] = type(
            "Config",
            (CustomConfig,),
            {"extra": getattr(CustomConfig, "extra", Extra.forbid)},
        )

        ValidatedFunctionBaseModel: Type[BaseModel] = type(
            "ValidatedFunctionBaseModel", (BaseModel,), {"Config": Config}
        )

        return create_model(
            to_camel(self.function.__name__),
            __base__=ValidatedFunctionBaseModel,
            **fields,
        )

    def bind_arguments(
        self, args: Tuple[Any, ...], kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build the arguments required to instantiate the model

        For example:
            def say(message: str, shout: bool = False):
                ...
        would generate the model:
            class Say(BaseModel):
                message: str
                shout: bool = False
        and when invoked as:
            say("hello")
        would generate "values" of:
            {"message": "hello"}
        """
        # TODO: Throw an exception if a required argument is missing (for when Field() used)
        # E.g:
        #   def greet(name: str = Field(...)):
        #       ...
        #   greet() # throw!

        # NOTE: Support aliases?
        # E.g:
        #   def greet(name: str = Field(alias="nom")):
        #       ...
        #   greet(nom="sam")

        # TODO: Throw the following TypeErrors:
        #   * n positional arguments expected but k given
        #   * unexpected keyword argument(s): 'foo', 'bar'
        #   * positional-only arguments passed as keyword arguments: 'foo', 'bar'
        #   * multiple values for arguments: 'foo', 'bar'

        return signature(self.function).bind(*args, **kwargs).arguments

    def prepare_arguments(
        self, arguments: Dict[str, Any], /
    ) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
        args: List[Any] = []
        kwargs: Dict[str, Any] = {}

        parameter: Parameter
        for parameter in self.parameters.values():
            argument: Any = arguments[parameter.name]

            if parameter.kind in (
                Parameter.POSITIONAL_ONLY,
                Parameter.POSITIONAL_OR_KEYWORD,
            ):
                args.append(argument)
            elif parameter.kind == Parameter.KEYWORD_ONLY:
                kwargs[parameter.name] = argument
            elif parameter.kind == Parameter.VAR_POSITIONAL:
                args.extend(argument)
            elif parameter.kind == Parameter.VAR_KEYWORD:
                kwargs.update(argument)

        return (tuple(args), kwargs)

    def call(self, *args: PS.args, **kwargs: PS.kwargs) -> RT:
        bound_arguments: Dict[str, Any] = self.bind_arguments(args, kwargs)
        model: BaseModel = self.model(**bound_arguments)
        arguments: Dict[str, Any] = model.dict()

        validated_args: Tuple[Any, ...]
        validated_kwargs: Dict[str, Any]
        validated_args, validated_kwargs = self.prepare_arguments(arguments)

        return self.function(*validated_args, **validated_kwargs)

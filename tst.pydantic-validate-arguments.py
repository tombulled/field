from dataclasses import dataclass
from typing import Any, Callable, Dict, Tuple

from pydantic import BaseModel
from pydantic.decorator import ValidatedFunction
from pydantic.fields import ModelField

from param import Param

"""
get_parameters() -> Dict[str, ModelField]
get_arguments(args, kwargs) -> Dict[str, Any]
call(args, kwargs) -> Any
"""


class CustomValidatedFunction(ValidatedFunction):
    pass


@dataclass
class ParameterisedFunction:
    function: Callable

    def get_parameters(self) -> Dict[str, ModelField]:
        validated_function: ValidatedFunction = ValidatedFunction(self.function, None)

        return {
            field_name: field
            for field_name, field in validated_function.model.__fields__.items()
            if not field_name.startswith("v__") and field_name not in ("args", "kwargs")
        }

    def get_arguments(
        self, args: Tuple[Any, ...], kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        validated_function: ValidatedFunction = ValidatedFunction(self.function, None)

        values: Dict[str, Any] = validated_function.build_values(args, kwargs)
        model: BaseModel = validated_function.model(**values)

        return self._modified_exec_to_get_args(model)

    def get_literal_arguments(
        self, args: Tuple[Any, ...], kwargs: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        validated_function: ValidatedFunction = ValidatedFunction(self.function, None)

        values: Dict[str, Any] = validated_function.build_values(args, kwargs)
        model: BaseModel = validated_function.model(**values)

        def captor(*_args, **_kwargs):
            return (_args, _kwargs)

        validated_function.raw_function = captor
        return validated_function.execute(model)

    def _modified_exec_to_get_args(self, model: BaseModel) -> Dict[str, Any]:
        validated_function: ValidatedFunction = ValidatedFunction(self.function, None)

        values: Dict[str, Any] = {
            key: value
            for key, value in model._iter()
            if key in model.__fields_set__ or model.__fields__[key].default_factory
        }
        var_kwargs = values.pop(validated_function.v_kwargs_name, {})

        args: Dict[str, Any] = {}
        kwargs: Dict[str, Any] = {}

        name: str
        value: Any

        if validated_function.v_args_name in values:
            in_kwargs: bool = False

            for name, value in values.items():
                if in_kwargs:
                    kwargs[name] = value
                elif name == validated_function.v_args_name:
                    args[name] = value
                    in_kwargs = True
                else:
                    args[name] = value

            return {**args, **kwargs, **var_kwargs}
        elif validated_function.positional_only_args:
            for name, value in values.items():
                if name in validated_function.positional_only_args:
                    args[name] = value
                else:
                    kwargs[name] = value

            return {**args, **kwargs, **var_kwargs}
        else:
            return {**values, **var_kwargs}

    def call(self, args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> Any:
        parameters: Dict[str, ModelField] = self.get_parameters()
        arguments: Dict[str, Any] = self.get_arguments(args, kwargs)
        literal_arguments: Tuple[
            Dict[str, Any], Dict[str, Any]
        ] = self.get_literal_arguments(args, kwargs)

        for field_name, value in arguments.items():
            field: ModelField = parameters[field_name]

            print(field_name, repr(value), repr(field))

        return self.function(*literal_arguments[0], **literal_arguments[1])


# @validate_arguments
def get(
    url: str, /, params: dict = Param(default_factory=dict), param: int = Param(123)
) -> dict:
    return dict(url=url, params=params, param=param)


# d = get("/foo")
# d2 = get("/bar", {"name": "sam"})
# d3 = get(123)
# d4 = get("/baz", "waffles")

vf = ValidatedFunction(get, None)
pf = ParameterisedFunction(get)

p = pf.get_parameters()
a = pf.get_arguments((123,), {})
a2 = pf.get_literal_arguments((123,), {})
# m = vf.model(url="/foo")
# a2 = pf._modified_exec_to_get_args(m)
d = pf.call((123,), {})

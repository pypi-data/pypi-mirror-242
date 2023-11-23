import typing
from contextlib import suppress

from pydantic import BaseModel

from mongo_path.field_repr import FieldStrs
from mongo_path.typing_utils import is_union, is_list_type


def get_field_from_args(args: typing.Iterable):
    for arg in args:
        if arg is not None:
            return arg


def generate_mongo_path_class(
    mongo_path: typing.Callable | FieldStrs,
    model: type | typing.Type[BaseModel],
    prefix=None,
):
    for field_name in model.model_fields:
        info = model.model_fields[field_name]
        field_type = info.annotation

        new_prefix = f"{prefix}." if prefix else ""

        field = FieldStrs(
            alias=info.alias,
            name=field_name,
            serialization_alias=info.serialization_alias,
            validation_alias=info.validation_alias.__str__(),
            prefix=new_prefix,
        )

        if is_union(field_type):
            args = typing.get_args(field_type)
            field_type = get_field_from_args(args)

        if is_list_type(field_type):
            args = typing.get_args(field_type)
            field_type = get_field_from_args(args)
            field = [field]  # type: ignore[assignment]

        with suppress(TypeError):
            if field_type and issubclass(field_type, BaseModel):
                generate_mongo_path_class(
                    field, field_type, prefix=f"{new_prefix}{field_name}"
                )
        try:
            mongo_path.__dict__.update({field_name: field})  # type: ignore[attr-defined]
        except AttributeError:
            mongo_path[0].__dict__.update({field_name: field})  # type: ignore[index]


def create_fields_from_model(model: type) -> typing.Callable:
    o = lambda: None
    generate_mongo_path_class(o, model)
    return o

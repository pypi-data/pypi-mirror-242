from typing import Any

from pydantic._internal._generics import PydanticGenericMetadata
from pydantic._internal._model_construction import ModelMetaclass

from mongo_path.path_generator import create_fields_from_model


class MongoMeta(ModelMetaclass):
    def __new__(
        cls,
        name,
        bases,
        attrs,
        __pydantic_generic_metadata__: PydanticGenericMetadata | None = None,
        __pydantic_reset_parent_namespace__: bool = True,
        **kwargs: Any,
    ):
        super_class = super().__new__(
            cls,
            name,
            bases,
            attrs,
            __pydantic_generic_metadata__,
            __pydantic_reset_parent_namespace__,
            **kwargs,
        )
        o = create_fields_from_model(super_class)
        for k in o.__dict__:
            setattr(super_class, k, o.__dict__[k])
        return super_class

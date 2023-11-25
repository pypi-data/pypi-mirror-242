from types import UnionType
from typing import get_origin, Union


def is_union(o: object) -> bool:
    origin = get_origin(o)
    return origin is Union or origin is UnionType


def is_list_type(field_type: type) -> bool:
    return get_origin(field_type) is list

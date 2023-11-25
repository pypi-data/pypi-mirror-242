from enum import Enum


class FieldAlias(Enum):
    no_alias = 0
    validation = 1
    serialization = 2
    alias = 3


class FieldStrs:
    def __init__(
        self, name, alias, validation_alias, serialization_alias, prefix
    ):
        self._prefix = prefix
        self._serialization_alias = serialization_alias
        self._validation_alias = validation_alias
        self._alias = alias
        self.__name = name

    def __str__(self, alias_type: FieldAlias = FieldAlias.no_alias):
        if alias_type == FieldAlias.validation:
            str_repr = self._validation_alias
        elif alias_type == FieldAlias.serialization:
            str_repr = self._serialization_alias
        elif alias_type == FieldAlias.alias:
            str_repr = self._alias
        else:
            str_repr = self.__name
        return f"{self._prefix}{str_repr}"


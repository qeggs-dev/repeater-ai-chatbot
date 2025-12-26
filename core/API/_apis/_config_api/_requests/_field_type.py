from enum import StrEnum


class FieldType(StrEnum):
    """FieldType Enum"""

    INT = "int"
    FLOAT = "float"
    STRING = "string"
    BOOLEAN = "boolean"
    DICT = "dict"
    LIST = "list"
    RAW = "raw"
    NULL = "null"
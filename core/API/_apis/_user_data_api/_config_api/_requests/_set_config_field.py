from pydantic import BaseModel
from typing import Any
from ._field_type import FieldType

class SetConfigRequest(BaseModel):
    value: Any
    type: FieldType = FieldType.RAW
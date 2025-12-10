from pydantic import BaseModel
from typing import Any

class SetConfigRequest(BaseModel):
    value: Any
    type: str
from pydantic import BaseModel, Field
from typing import Any

class SystemInfo(BaseModel):
    extra_info: dict[str, Any] = Field(default_factory=dict)
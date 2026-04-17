from .....Assist_Struct import RequestUserInfo
from pydantic import BaseModel, Field
from typing import Any

class ExpandVariableRequest(BaseModel):
    user_info: RequestUserInfo = Field(default_factory=RequestUserInfo)
    text: str
    extra_fields: dict[str, Any] = Field(default_factory=dict)
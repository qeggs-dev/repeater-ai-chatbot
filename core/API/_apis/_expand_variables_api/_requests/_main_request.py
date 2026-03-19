from .....Assist_Struct import Request_User_Info
from pydantic import BaseModel, Field
from typing import Any

class ExpandVariableRequest(BaseModel):
    user_info: Request_User_Info = Field(default_factory=Request_User_Info)
    text: str
    expand_fields: dict[str, Any] = Field(default_factory=dict)
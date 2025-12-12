from .....Request_User_Info import Request_User_Info
from pydantic import BaseModel, Field

class ExpandVariableRequest(BaseModel):
    user_info: Request_User_Info = Field(default_factory=Request_User_Info)
    text: str
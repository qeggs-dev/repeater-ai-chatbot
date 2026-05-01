from pydantic import BaseModel, Field

class UserInfo(BaseModel):
    generated_length: int = 0

class TasksIDResponse(BaseModel):
    message: str = ""
    count: int = 0
    users: dict[str, UserInfo] = Field(default_factory=dict)
from pydantic import BaseModel, ConfigDict

class Request_User_Info(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
    )

    username: str | None = None
    nickname: str | None = None
    age: int | float | None = None
    gender: str | None = None
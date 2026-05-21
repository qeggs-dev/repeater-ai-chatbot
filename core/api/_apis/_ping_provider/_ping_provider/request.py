from pydantic import BaseModel

class PingRequest(BaseModel):
    model_uid: str | list[str] | None = None
    timeout: float | None = None
    times: int | None = None
    size: int | None = None
    interval: int | None = None
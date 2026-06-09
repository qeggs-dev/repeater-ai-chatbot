from pydantic import BaseModel

class PingRequest(BaseModel):
    model_id: str | list[str] | None = None
    timeout: int | float | None = None
    times: int | None = None
    size: int | None = None
    interval: int | float | None = None
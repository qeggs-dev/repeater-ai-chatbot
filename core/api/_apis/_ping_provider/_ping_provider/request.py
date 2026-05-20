from pydantic import BaseModel

class PingRequest(BaseModel):
    timeout: float = 5.0
    times: int = 4
    size: int = 32
    interval: int = 0
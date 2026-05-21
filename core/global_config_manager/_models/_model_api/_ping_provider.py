from pydantic import BaseModel

class PingProvider(BaseModel):
    timeout: int = 2
    times: int = 4
    size: int = 32
    interval: int = 0
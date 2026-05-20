from pydantic import BaseModel, Field

class PingDetail(BaseModel):
    host: str = ""
    time: list[float] = Field(default_factory=list)

class PingResponse(BaseModel):
    successful: int = 0
    average_time_spent: float = 0.0
    details: list[PingDetail] = Field(default_factory=list) 
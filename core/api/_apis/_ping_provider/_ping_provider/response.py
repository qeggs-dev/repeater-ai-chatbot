from pydantic import BaseModel, Field

class PingDetail(BaseModel):
    host: str = ""
    time: list[float] = Field(default_factory=list)
    packet_loss: float = 0.0
    max_time: float = 0.0
    min_time: float = 0.0
    avg_time: float = 0.0

class PingResponse(BaseModel):
    successful: int = 0
    average_time_spent: float = 0.0
    details: list[PingDetail] = Field(default_factory=list) 
from pydantic import BaseModel, Field

class Detail(BaseModel):
    host: str = ""
    time: list[float] = Field(default_factory=list)

class Response(BaseModel):
    successful: int = 0
    average_time_spent: float = 0.0
    details: list[Detail] = Field(default_factory=list) 
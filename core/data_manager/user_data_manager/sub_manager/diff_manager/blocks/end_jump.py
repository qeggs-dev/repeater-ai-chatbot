import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal

class EndJumpModel(BaseModel):
    type: Literal["end_jump"] = "end_jump"
    target_file: str
    time: datetime = Field(default_factory=datetime.now)
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
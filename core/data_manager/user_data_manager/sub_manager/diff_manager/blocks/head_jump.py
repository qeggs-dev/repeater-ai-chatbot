import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal

class HeadJumpModel(BaseModel):
    type: Literal["head_jump"] = "head_jump"
    target_file: str | None = Field(None)
    time: datetime = Field(default_factory=datetime.now)
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
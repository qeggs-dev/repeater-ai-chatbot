import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, Literal

class SnapShotModel(BaseModel):
    type: Literal["snapshot"] = "snapshot"
    data: Any
    time: datetime = Field(default_factory=datetime.now)
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, Literal

class DiffModel(BaseModel):
    type: Literal["diff"] = "diff"
    diff: Any
    rdiff: Any = Field(default=None)
    time: datetime = Field(default_factory=datetime.now)
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
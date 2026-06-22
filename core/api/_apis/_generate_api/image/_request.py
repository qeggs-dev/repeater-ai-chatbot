from pydantic import BaseModel, ConfigDict, Field
from typing import Any

from .....auxiliary.http import (
    ClientLimits,
    ClientTimeout
)

class Request(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True
    )
    
    model_id: str | None = None
    prompt: str = ""
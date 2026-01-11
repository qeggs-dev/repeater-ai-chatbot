from pydantic import BaseModel, Field
from typing import Any

class RaiseErrorRequest(BaseModel):
    """
    Request model for raising an error.
    """
    type: str
    args: list[str] = Field(default_factory=list)
    kwargs: dict[str, Any] = Field(default_factory=dict)
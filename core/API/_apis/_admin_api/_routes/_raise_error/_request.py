from pydantic import BaseModel
from typing import Any

class RaiseErrorRequest(BaseModel):
    """
    Request model for raising an error.
    """
    error_type: str
    error_args: list[str]
    error_kwargs: dict[str, Any]
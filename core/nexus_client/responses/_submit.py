from pydantic import BaseModel
from typing import Any

class SubmitResponse(BaseModel):
    """
    Submit Response Model
    """
    status: str = ""
    message: str = ""
    resource_uuid: str = ""
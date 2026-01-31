from pydantic import BaseModel
from typing import Any

class SubmitResponse(BaseModel):
    """
    Submit Response Model
    """
    status: str = ""
    file_uuid: str = ""
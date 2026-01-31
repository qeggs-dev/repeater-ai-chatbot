from pydantic import BaseModel
from typing import Any

class DownloadResponse(BaseModel):
    """
    Download Response
    """
    status: str = ""
    message: str = ""
    data: Any | None = None
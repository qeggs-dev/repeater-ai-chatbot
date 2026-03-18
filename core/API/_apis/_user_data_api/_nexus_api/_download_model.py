from pydantic import BaseModel
from typing import Any

class DownloadRequest(BaseModel):
    id: str

class DownloadResponse(BaseModel):
    message: str = ""
    nexus_message: str | Any = ""
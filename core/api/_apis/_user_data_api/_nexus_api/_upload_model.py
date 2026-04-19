from pydantic import BaseModel
from typing import Any

class UploadRequest(BaseModel):
    timeout: int | None = None

class UploadResponse(BaseModel):
    message: str = ""
    nexus_message: str | Any = ""
    resource_uuid: str | None = None
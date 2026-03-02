from pydantic import BaseModel

class UploadRequest(BaseModel):
    timeout: int | None = None

class UploadResponse(BaseModel):
    message: str = ""
    nexus_message: str = ""
    file_uuid: str | None = None
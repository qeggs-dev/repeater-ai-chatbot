from pydantic import BaseModel

class DownloadRequest(BaseModel):
    id: str

class DownloadResponse(BaseModel):
    message: str = ""
    nexus_message: str = ""
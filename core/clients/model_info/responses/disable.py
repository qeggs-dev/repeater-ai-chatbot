from pydantic import BaseModel

class DisableResponse(BaseModel):
    message: str = ""
    success: int = 0
    total: int = 0
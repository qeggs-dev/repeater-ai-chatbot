from pydantic import BaseModel

class UpdateResponse(BaseModel):
    """
    Update Response
    """
    status: str = ""
    message: str = ""
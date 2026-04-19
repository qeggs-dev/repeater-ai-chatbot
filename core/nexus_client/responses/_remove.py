from pydantic import BaseModel

class RemoveResponse(BaseModel):
    """
    Remove Response
    """
    status: str = ""
    message: str = ""
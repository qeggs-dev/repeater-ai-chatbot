from pydantic import BaseModel

class RaiseWarningRequest(BaseModel):
    """
    Request model for raising an warning.
    """
    type: str
    message: str = ""
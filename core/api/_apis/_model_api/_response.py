from pydantic import BaseModel, Field
from ....clients.model_info import SafeModelInfo

class ResponseModel(BaseModel):
    """
    Base response model
    """
    message: str = ""
    models: list[SafeModelInfo] = Field(default_factory=list)
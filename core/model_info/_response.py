from pydantic import BaseModel, Field
from ._models import ModelInfo

class ModelInfoResponse(BaseModel):
    message: str = ""
    models: list[ModelInfo] = Field(default_factory=list)
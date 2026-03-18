from pydantic import BaseModel, ConfigDict, Field
from ._model_type import ModelType

class StaticModelAPI(BaseModel):
    name: str = ""
    url: str = ""
    id: str = ""
    api_key: str = ""
    parent: str = ""
    uid: str = ""
    type: ModelType = ModelType.CHAT
    timeout: float = 600.0

class ModelAPI(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True
    )

    name: str = ""
    url: str = ""
    id: str = ""
    parent: str = ""
    uid: str = ""
    type: ModelType = ModelType.CHAT
    timeout: float = 600.0

class ModelsResponse(BaseModel):
    message: str = ""
    models: list[ModelAPI | StaticModelAPI] = Field(default_factory=list)

class APIKeyResponse(BaseModel):
    message: str = ""
    api_keys: list[str] = Field(default_factory=list)

class ExceptionResponse(BaseModel):
    message: str = ""
    exception: str = ""
    timestamp: float = 0.0
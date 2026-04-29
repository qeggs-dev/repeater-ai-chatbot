from pydantic import BaseModel, ConfigDict, Field
from .models import ModelAPIData

class SafeModelInfo(BaseModel):
    name: str = ""
    uid: str = ""
    parent: str = ""
    timeout: float = 600.0
    detailed: ModelAPIData | None = None

class ModelInfo(BaseModel):
    name: str = ""
    url: str = ""
    proxy: str | None = None
    id: str = ""
    uid: str = ""
    api_key: str | None = None
    parent: str = ""
    detailed: ModelAPIData = Field(default_factory=ModelAPIData)
    timeout: float = 600.0

    def to_safe(self, detailed_info: bool = False) -> SafeModelInfo:
        return SafeModelInfo(
            name = self.name,
            uid = self.uid,
            parent = self.parent,
            timeout = self.timeout,
            detailed = self.detailed if detailed_info else None
        )
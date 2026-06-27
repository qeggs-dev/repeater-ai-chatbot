from urllib.parse import urljoin
from pydantic import BaseModel, ConfigDict, Field
from ...auxiliary.http import ClientLimits, ClientTimeout
from .models import ModelAPIData

class SafeModelInfo(BaseModel):
    name: str = ""
    uid: str = ""
    parent: str = ""
    parent_id: str = ""
    timeout: float | ClientTimeout = 600.0
    detailed: ModelAPIData | None = None

class ModelInfo(BaseModel):
    base_url: str = ""
    endpoint: str = ""
    fetch_models_endpoint: str = "/models"
    proxy: str | None = None
    limits: ClientLimits = Field(default_factory=ClientLimits)
    timeout: float | ClientTimeout = Field(default=600.0)
    
    name: str = ""
    id: str = ""
    uid: str = ""
    api_key: str | None = None
    parent: str = ""
    parent_id: str = ""
    detailed: ModelAPIData = Field(default_factory=ModelAPIData)

    def to_safe(self, detailed_info: bool = False) -> SafeModelInfo:
        return SafeModelInfo(
            name = self.name,
            uid = self.uid,
            parent = self.parent,
            parent_id = self.parent_id,
            timeout = self.timeout,
            detailed = self.detailed if detailed_info else None
        )
    
    def get_base_url(self) -> str:
        if self.endpoint:
            return urljoin(self.base_url, self.endpoint)
        return self.base_url
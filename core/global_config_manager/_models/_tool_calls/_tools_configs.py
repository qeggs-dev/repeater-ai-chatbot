from pydantic import BaseModel, Field
from .tools_configs import (
    HTTPRequests,
    Asteval,
    SystemInfo
)

class ToolsConfigs(BaseModel):
    http_requests: HTTPRequests = Field(default_factory=HTTPRequests)
    asteval: Asteval = Field(default_factory=Asteval)
    system_info: SystemInfo = Field(default_factory=SystemInfo)
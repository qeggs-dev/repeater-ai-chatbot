from pydantic import BaseModel, Field
from .tools_configs import (
    HTTPRequests,
    SystemInfo
)

class ToolsConfigs(BaseModel):
    http_requests: HTTPRequests = Field(default_factory=HTTPRequests)
    system_info: SystemInfo = Field(default_factory=SystemInfo)
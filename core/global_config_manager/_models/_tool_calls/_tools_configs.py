from pydantic import BaseModel, Field
from ._http_request import HTTPRequests

class ToolsConfigs(BaseModel):
    http_requests: HTTPRequests = Field(default_factory=HTTPRequests)
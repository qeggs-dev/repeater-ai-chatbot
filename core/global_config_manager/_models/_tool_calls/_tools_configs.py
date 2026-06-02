from pydantic import BaseModel, Field
from ._http_request import HTTPRequest

class ToolsConfigs(BaseModel):
    http_request: HTTPRequest = Field(default_factory=HTTPRequest)
from pydantic import BaseModel, Field
from ._http_request import HTTPRequests
from ._asteval import Asteval

class ToolsConfigs(BaseModel):
    http_requests: HTTPRequests = Field(default_factory=HTTPRequests)
    asteval: Asteval = Field(default_factory=Asteval)
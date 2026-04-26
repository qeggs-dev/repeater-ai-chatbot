from pydantic import BaseModel, Field
from ._http_methods import HTTPMethods
from typing import Literal

class ToolCallsConfigs(BaseModel):
    enabled: bool = True
    registed: set[str] = Field(default_factory=list)
    allow_by_default: bool = False
    result_max_length_for_logs: int | None = 100
    allowed_http_methods: list[HTTPMethods] | Literal["ALL"] | None = None
    allow_private_network_requests: bool = False
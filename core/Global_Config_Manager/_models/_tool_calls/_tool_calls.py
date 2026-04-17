from pydantic import BaseModel, Field
from ._http_methods import HTTPMethods
from typing import Literal

class ToolCallsConfigs(BaseModel):
    enabled: bool = True
    registed: list[str] = Field(default_factory=list)
    result_max_length_for_logs: int | None = 100
    allowed_http_methods: list[HTTPMethods] | Literal["ALL"] | None = None
    allow_private_network_requests: bool = False
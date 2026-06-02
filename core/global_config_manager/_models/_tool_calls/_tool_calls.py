from pydantic import BaseModel, Field, field_serializer
from ._http_methods import HTTPMethods
from typing import Literal

class ToolCallsConfigs(BaseModel):
    enabled: bool = True
    registed: set[str] = Field(default_factory=set)
    crawler_name: str = "Repeater AI Crawler"
    allowed_by_default: set[str] = Field(default_factory=set)
    result_max_length_for_logs: int | None = 100
    allowed_http_methods: list[HTTPMethods] | Literal["ALL"] | None = None
    allow_private_network_requests: bool = False

    @field_serializer("registed", mode = "plain")
    def registed_serializer(self, value: set[str]) -> list[str]:
        return list(value)
    
    @field_serializer("allowed_by_default", mode = "plain")
    def allowed_by_default_serializer(self, value: set[str]) -> list[str]:
        return list(value)
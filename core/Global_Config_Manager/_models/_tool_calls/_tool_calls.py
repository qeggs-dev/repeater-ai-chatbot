from pydantic import BaseModel

class ToolCallsConfigs(BaseModel):
    enabled: bool = True
    result_max_length_for_logs: int | None = 100
    allow_all_http_methods: bool = False
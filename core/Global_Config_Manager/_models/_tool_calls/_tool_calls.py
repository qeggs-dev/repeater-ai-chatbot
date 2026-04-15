from pydantic import BaseModel

class ToolCallsConfigs(BaseModel):
    enabled: bool = True
    result_max_length_for_logs: int = 10
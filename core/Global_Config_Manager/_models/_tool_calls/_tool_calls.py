from pydantic import BaseModel

class ToolCallsConfigs(BaseModel):
    enabled: bool = True
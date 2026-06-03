from pydantic import BaseModel, Field

class SystemInfo(BaseModel):
    extra_info: dict[str, str] = Field(default_factory=dict)
from pydantic import BaseModel, ConfigDict, Field

class CallAPIConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    max_concurrency: int = 1000
    include_usage: bool | None = None
    include_obfuscation: bool | None = None
    max_regenerate_times: int = Field(default=10, ge=1)
    send_user_id: bool = False
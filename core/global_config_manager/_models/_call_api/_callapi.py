from pydantic import BaseModel, ConfigDict, Field

class CallAPIConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    max_concurrency: int = 1024
    client_cache_size: int = 32
    include_usage: bool | None = None
    include_obfuscation: bool | None = None
    max_generate_times: int = Field(default=10, ge=1)
    failed_disable_timeout: int | float = Field(default=60, ge=1)
    send_user_id: bool = False
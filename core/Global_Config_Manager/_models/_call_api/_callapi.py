from pydantic import BaseModel, ConfigDict

class CallAPI_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    max_concurrency: int = 1000
    include_usage: bool | None = None
    include_obfuscation: bool | None = None
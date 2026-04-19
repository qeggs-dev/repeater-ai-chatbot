from pydantic import BaseModel, ConfigDict

class CacheDataConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    context: bool = False
    prompt: bool = False
    config: bool = False
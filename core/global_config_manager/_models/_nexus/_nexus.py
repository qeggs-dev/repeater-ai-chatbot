from pydantic import BaseModel, ConfigDict

class NexusConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    base_url: str = ""
    api_timeout: int | float = 60
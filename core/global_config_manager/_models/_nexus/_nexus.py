from pydantic import BaseModel, ConfigDict

class NexusConfig(BaseModel):
    base_url: str = ""
    api_timeout: int | float | None = 60
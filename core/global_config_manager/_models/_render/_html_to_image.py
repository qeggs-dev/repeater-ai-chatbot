from pydantic import BaseModel, ConfigDict, Field

class HTMLToImageConfig(BaseModel):
    base_url: str = Field(default="")
    timeout: int | float = Field(default=600.0)
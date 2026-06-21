from pydantic import BaseModel, ConfigDict

class HTMLToImageConfig(BaseModel):
    base_url: str = ""
    timeout: int = 600.0
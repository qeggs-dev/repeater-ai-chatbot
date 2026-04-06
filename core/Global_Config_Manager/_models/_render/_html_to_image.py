from pydantic import BaseModel, ConfigDict

class HTMLToImageConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    base_url: str = ""
    timeout: int = 600.0
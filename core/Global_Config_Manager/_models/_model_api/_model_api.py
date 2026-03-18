from pydantic import BaseModel, ConfigDict

class ModelAPIConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)
    
    base_url: str = ""
    timeout: int | float | None = 10.0
    default_model_uid: str = "chat"
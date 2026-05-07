from pydantic import BaseModel, ConfigDict

class ModelAPIConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)
    
    base_url: str = ""
    timeout: int | float | None = 10.0
    api_key_env_name: str = "MODEL_INFO_API_KEY"
    default_model_uid: str | list[str] = "chat"
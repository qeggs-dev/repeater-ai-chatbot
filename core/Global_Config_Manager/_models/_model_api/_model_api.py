from pydantic import BaseModel, ConfigDict

class Model_API_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)
    
    api_file_path: str = "./configs/api_info.json"
    default_model_uid: str = "chat"
    case_sensitive: bool = False
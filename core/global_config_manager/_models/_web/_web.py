from pydantic import BaseModel, ConfigDict

class WebConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    index_web_file: str = ""
    web_directory: str = "./configs/web"
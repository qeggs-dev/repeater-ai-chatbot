from pydantic import BaseModel, ConfigDict

class WebConfig(BaseModel):
    index_web_file: str = ""
    web_directory: str = "./configs/web"
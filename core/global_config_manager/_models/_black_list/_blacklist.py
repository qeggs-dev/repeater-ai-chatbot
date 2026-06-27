from pydantic import BaseModel, ConfigDict


class BacklistConfig(BaseModel):
    file_path: str = "./configs/blacklist.regex"
    match_timeout: float = 10.0
from pydantic import BaseModel, ConfigDict


class UserNicknameMappingConfig(BaseModel):
    file_path: str = "./configs/user_nickname_mapping.json"
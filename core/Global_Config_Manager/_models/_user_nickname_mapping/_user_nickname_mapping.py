from pydantic import BaseModel, ConfigDict


class UserNicknameMappingConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    file_path: str = "./configs/user_nickname_mapping.json"
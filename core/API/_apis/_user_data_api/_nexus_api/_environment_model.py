from pydantic import BaseModel
from .....User_Config_Manager import UserConfigs

class EnvironmentModel(BaseModel):
    context: list
    prompt: str
    config: UserConfigs
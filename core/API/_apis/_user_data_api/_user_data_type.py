from enum import StrEnum
from ..._resource import Resource
from ....Data_Manager import UserDataManager

class UserDataType(StrEnum):
    CONTEXT = "context"
    PROMPT = "prompt"
    CONFIG = "config"

def get_manager(data_type: UserDataType) -> UserDataManager:
    match data_type:
        case UserDataType.CONTEXT:
            return Resource.core.context_manager
        case UserDataType.PROMPT:
            return Resource.core.prompt_manager
        case UserDataType.CONFIG:
            return Resource.core.user_config_manager
    
    raise ValueError(f"Invalid data type: {data_type}")
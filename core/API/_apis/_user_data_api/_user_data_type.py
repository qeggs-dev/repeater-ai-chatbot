from enum import StrEnum
from ....Server import Server
from ....Data_Manager import UserDataManager

class UserDataType(StrEnum):
    CONTEXT = "context"
    PROMPT = "prompt"
    CONFIG = "config"

def get_manager(data_type: UserDataType) -> UserDataManager:
    match data_type:
        case UserDataType.CONTEXT:
            return Server.core.context_manager
        case UserDataType.PROMPT:
            return Server.core.prompt_manager
        case UserDataType.CONFIG:
            return Server.core.user_config_manager
    
    raise ValueError(f"Invalid data type: {data_type}")
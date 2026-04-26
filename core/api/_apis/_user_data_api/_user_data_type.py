from enum import StrEnum
from ....server import Server
from ....data_manager import UserDataManager

class UserDataType(StrEnum):
    CONTEXT = "context"
    PROMPT = "prompt"
    CONFIG = "config"

def get_manager(data_type: UserDataType) -> UserDataManager:
    match data_type:
        case UserDataType.CONTEXT:
            return Server.core.runtime.context_manager
        case UserDataType.PROMPT:
            return Server.core.runtime.prompt_manager
        case UserDataType.CONFIG:
            return Server.core.runtime.user_config_manager
    
    raise ValueError(f"Invalid data type: {data_type}")
from pydantic import BaseModel, ValidationError
from typing import TypeGuard, Any

class ConfigForceLoadList(BaseModel):
    force_load_list: list[str]

def is_config_force_load_list(o: list[str] | Any) -> TypeGuard[list[str]]:
    try:
        ConfigForceLoadList(
            force_load_list = o
        )
        return True
    except ValidationError:
        return False
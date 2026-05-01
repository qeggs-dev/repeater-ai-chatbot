from ......global_config_manager import ConfigManager
from ......server import Server
from ......special_exception import HTTPException
from fastapi import (
    Header
)
from fastapi.responses import ORJSONResponse

@Server.app.get("/admin/debug/get_configs")
async def get_configs(
        api_key: str = Header(..., alias="X-Admin-API-Key")
    ):
    """
    This API is used to collapse the server.
    """
    if not Server.admin_key_manager.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    
    return ORJSONResponse(
        ConfigManager.get_configs().model_dump()
    )
from ......Global_Config_Manager import ConfigManager
from ......_server import Server
from fastapi import (
    HTTPException,
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
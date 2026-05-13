from ......global_config_manager import ConfigManager
from fastapi.responses import ORJSONResponse
from ..._admin_router import admin_router

@admin_router.get("/debug/get_configs")
async def get_configs():
    """
    This API is used to collapse the server.
    """
    
    return ORJSONResponse(
        ConfigManager.get_configs().model_dump()
    )
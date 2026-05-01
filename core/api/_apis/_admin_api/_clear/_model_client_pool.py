from .....global_config_manager import ConfigManager
from .....server import Server
from .....special_exception import HTTPException
from fastapi import (
    Header
)
from fastapi.responses import ORJSONResponse
from .....runtime_container import RuntimeContainer

@Server.app.get("/admin/clear/model_client_pool")
async def get_configs(
        api_key: str = Header(..., alias="X-Admin-API-Key")
    ):
    """
    This API is used to collapse the server.
    """
    if not Server.admin_key_manager.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    RuntimeContainer.get_runtime().openai_pool.clear()
    RuntimeContainer.get_runtime().openai_pool.reset_cache_stats()
    return ORJSONResponse(
        ConfigManager.get_configs().model_dump()
    )
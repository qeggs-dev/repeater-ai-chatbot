from .....global_config_manager import ConfigManager
from .....server import Server
from .....special_exception import HTTPException
from fastapi import (
    Header
)
from fastapi.responses import ORJSONResponse
from .....runtime_container import RuntimeContainer
from .._admin_router import admin_router

@admin_router.get("/clear/model_client_pool")
async def clear_model_client_pool():
    """
    This API is used to collapse the server.
    """
    RuntimeContainer.get_runtime().openai_pool.clear()
    RuntimeContainer.get_runtime().openai_pool.reset_cache_stats()
    return ORJSONResponse(
        ConfigManager.get_configs().model_dump()
    )
from .....global_config_manager import ConfigManager
from fastapi.responses import ORJSONResponse
from .....runtime_container import RuntimeContainer
from .._admin_router import admin_router

@admin_router.get("/clear/model_client_pool")
async def clear_model_client_pool():
    """
    This API is used to collapse the server.
    """
    runtime = RuntimeContainer.get_runtime()
    runtime.openai_pool.clear()
    runtime.openai_pool.reset_cache_stats()
    return ORJSONResponse(
        ConfigManager.get_configs().model_dump()
    )
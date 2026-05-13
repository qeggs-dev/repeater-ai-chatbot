import asyncio
from fastapi import (
    Header
)
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger
from .....global_config_manager import ConfigManager
from .._admin_router import admin_router

@admin_router.post("/configs/reload")
async def reload_configs_api():
    """
    Reload Project Configs

    Warning: Some modules may cache configuration results, which could cause configuration differences!

    :param api_key: Admin API key
    """
    logger.info("Reloading configs", user_id="[Admin API]")
    await asyncio.to_thread(ConfigManager.load)
    return ORJSONResponse({"detail": "Configs reloaded"})
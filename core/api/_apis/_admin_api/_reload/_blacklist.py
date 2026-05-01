import asyncio
from .....server import Server
from .....special_exception import HTTPException
from fastapi import (
    Header
)
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger
from .....global_config_manager import ConfigManager
from .._admin_router import admin_router

@admin_router.post("/blacklist/reload")
async def reload_blacklist_api():
    """
    Reload blacklist

    :param api_key: Admin API key
    :return: JSON response
    """
    logger.info("Reloading blacklist", user_id="[Admin API]")
    await Server.core.load_blacklist()
    return ORJSONResponse({"detail": "Blacklist reloaded"})
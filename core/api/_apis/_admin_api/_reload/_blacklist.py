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

@Server.app.post("/admin/blacklist/reload")
async def reload_blacklist_api(api_key: str = Header(..., alias="X-Admin-API-Key")):
    """
    Reload blacklist

    :param api_key: Admin API key
    :return: JSON response
    """
    if not Server.admin_key_manager.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    logger.info("Reloading blacklist", user_id="[Admin API]")
    await Server.core.load_blacklist()
    return ORJSONResponse({"detail": "Blacklist reloaded"})
import asyncio
from ...._resource import Resource
from fastapi import (
    HTTPException,
    Header
)
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger
from .....Global_Config_Manager import ConfigManager

@Resource.app.post("/admin/apiinfo/reload")
async def reload_apiinfo_api(api_key: str = Header(..., alias="X-Admin-API-Key")):
    """
    Reload API information

    :param api_key: Admin API key
    :return: JSON response
    """
    if not Resource.admin_key_manager.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    logger.info("Reloading apiinfo", user_id="[Admin API]")
    await Resource.core.reload_apiinfo()
    return ORJSONResponse({"detail": "Apiinfo reloaded"})

@Resource.app.post("/admin/blacklist/reload")
async def reload_blacklist_api(api_key: str = Header(..., alias="X-Admin-API-Key")):
    """
    Reload blacklist

    :param api_key: Admin API key
    :return: JSON response
    """
    if not Resource.admin_key_manager.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    logger.info("Reloading blacklist", user_id="[Admin API]")
    await Resource.core.load_blacklist()
    return ORJSONResponse({"detail": "Blacklist reloaded"})

@Resource.app.post("/admin/configs/reload")
async def reload_configs_api(api_key: str = Header(..., alias="X-Admin-API-Key")):
    """
    Reload Project Configs

    Warning: Some modules may cache configuration results, which could cause configuration differences!

    :param api_key: Admin API key
    """
    if not Resource.admin_key_manager.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    logger.info("Reloading configs", user_id="[Admin API]")
    await asyncio.to_thread(ConfigManager.load)
    return ORJSONResponse({"detail": "Configs reloaded"})
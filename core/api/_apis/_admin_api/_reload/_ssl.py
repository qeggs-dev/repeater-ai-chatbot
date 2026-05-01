import ssl
import asyncio
from .....server import Server
from .....special_exception import (
    HTTPException
)
from fastapi import (
    Header
)
from fastapi.responses import (
    ORJSONResponse
)
from .....auxiliary.http import update_ssl_context
from loguru import logger
from .....global_config_manager import ConfigManager

@Server.app.post("/admin/configs/ssl")
async def reload_configs_api(api_key: str = Header(..., alias="X-Admin-API-Key")):
    """
    Reload Project SSL configuration

    Warning: Some modules may cache SSL certificates, which could cause configuration differences!

    :param api_key: Admin API key
    """
    if not Server.admin_key_manager.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    logger.info("Reloading SSL", user_id="[Admin API]")
    await asyncio.to_thread(update_ssl_context)
    return ORJSONResponse({"detail": "Configs reloaded"})
from .._resource import (
    app,
    admin_api_key,
    chat,
    configs
)
from fastapi import (
    HTTPException,
    Header
)
from fastapi.responses import (
    JSONResponse
)
from loguru import logger

@app.post("/admin/apiinfo/reload")
async def reload_apiinfo(api_key: str = Header(..., alias="X-Admin-API-Key")):
    """
    Reload API information

    :param api_key: Admin API key
    :return: JSON response
    """
    if not admin_api_key.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    logger.info("Reloading apiinfo", user_id="[Admin API]")
    await chat.reload_apiinfo()
    return JSONResponse({"detail": "Apiinfo reloaded"})

@app.post("/admin/blacklist/reload")
async def reload_blacklist(api_key: str = Header(..., alias="X-Admin-API-Key")):
    """
    Reload blacklist

    :param api_key: Admin API key
    :return: JSON response
    """
    if not admin_api_key.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    logger.info("Reloading blacklist", user_id="[Admin API]")
    await chat.load_blacklist()
    return JSONResponse({"detail": "Blacklist reloaded"})

@app.post("/admin/configs/reload")
async def reload_configs(api_key: str = Header(..., alias="X-Admin-API-Key")):
    """
    Reload Project Configs

    Warning: Some modules may cache configuration results, which could cause configuration differences!

    :param api_key: Admin API key
    """
    if not admin_api_key.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    logger.info("Reloading configs", user_id="[Admin API]")
    await configs.reload_config_async()
    return JSONResponse({"detail": "Apiinfo reloaded"})

@app.post("/admin/configs/{name}/seek/{index}")
async def seek_configs(name: str, index: int, api_key: str = Header(..., alias="X-Admin-API-Key")):
    """
    Endpoint for seek configs
    """
    if not admin_api_key.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    if configs.seek_config(name, index):
        logger.info(f"Seek {name}", user_id="[Admin API]")
        return JSONResponse({"detail": "Apiinfo reloaded"})
    else:
        logger.error(f"Seek {name} Failed", user_id="[Admin API]")
        return JSONResponse({"detail": "Seek Configs failed"}, status_code=400)

@app.post("/admin/regenerate/admin_key")
async def regenerate_admin_key(api_key: str = Header(..., alias="X-Admin-API-Key")):
    """
    Endpoint for regenerating admin key
    """
    if not admin_api_key.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    logger.info("Regenerating admin key", user_id="[Admin API]")
    admin_api_key.generate()
    return JSONResponse({"message": "Admin key regenerated", "admin_key": admin_api_key.api_key})
from ...._resource import Resource
from fastapi import (
    HTTPException,
    Header
)
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger

@Resource.app.post("/admin/admin_key/regenerate")
async def regenerate_admin_key_api(api_key: str = Header(..., alias="X-Admin-API-Key")):
    """
    Endpoint for regenerating admin key
    """
    if not Resource.admin_key_manager.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    logger.info("Regenerating admin key", user_id="[Admin API]")
    Resource.admin_key_manager.generate()
    return ORJSONResponse({"message": "Admin key regenerated", "admin_key": Resource.admin_key_manager.api_key})
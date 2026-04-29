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
from loguru import logger

@Server.app.post("/admin/admin_key/regenerate")
async def regenerate_admin_key_api(api_key: str = Header(..., alias="X-Admin-API-Key")):
    """
    Endpoint for regenerating admin key
    """
    if not Server.admin_key_manager.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    logger.info("Regenerating admin key", user_id="[Admin API]")
    Server.admin_key_manager.generate()
    return ORJSONResponse({"message": "Admin key regenerated", "admin_key": Server.admin_key_manager.api_key})
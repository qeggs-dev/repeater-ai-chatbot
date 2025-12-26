from ....._resource import (
    app,
    admin_api_key,
)
from fastapi import (
    HTTPException,
    Header
)
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger

@app.post("/admin/admin_key/regenerate")
async def regenerate_admin_key(api_key: str = Header(..., alias="X-Admin-API-Key")):
    """
    Endpoint for regenerating admin key
    """
    if not admin_api_key.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    logger.info("Regenerating admin key", user_id="[Admin API]")
    admin_api_key.generate()
    return ORJSONResponse({"message": "Admin key regenerated", "admin_key": admin_api_key.api_key})
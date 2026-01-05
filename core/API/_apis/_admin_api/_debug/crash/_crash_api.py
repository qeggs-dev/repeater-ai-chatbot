from ......CriticalException import CriticalException
import asyncio
from ....._resource import (
    app,
    admin_api_key,
    chat
)
from fastapi import (
    HTTPException,
    Header
)
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger

@app.post("/admin/debug/crash")
async def crash_api(
        api_key: str = Header(..., alias="X-Admin-API-Key")
    ):
    """
    This API is used to collapse the server.
    """
    if not admin_api_key.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    logger.info(
        "Manually causing a program crash.",
        user_id = "[Admin API]"
    )
    raise CriticalException(
        "A crash that is manually triggered by the administrator API. The program does not have an exception."
    )
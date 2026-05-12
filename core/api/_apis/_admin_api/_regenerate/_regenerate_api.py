from .....server import RepeaterMain
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger
from .._admin_router import admin_router

@admin_router.post("/admin_key/regenerate")
async def regenerate_admin_key_api():
    """
    Endpoint for regenerating admin key
    """
    logger.info("Regenerating admin key", user_id="[Admin API]")
    server = RepeaterMain.get_now_server()
    server.admin_key_manager.generate()
    return ORJSONResponse({"message": "Admin key regenerated", "admin_key": server.admin_key_manager.api_key})
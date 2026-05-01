from ......special_exception import CriticalException, HTTPException
from ......server import Server
from fastapi import (
    Header
)
from loguru import logger
from ..._admin_router import admin_router

@admin_router.post("/debug/crash")
async def crash_api():
    """
    This API is used to collapse the server.
    """
    logger.info(
        "Manually causing a program crash.",
        user_id = "[Admin API]"
    )
    raise CriticalException(
        "A crash that is manually triggered by the administrator API. The program does not have an exception."
    )
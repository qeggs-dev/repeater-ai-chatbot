import warnings
from ......server import Server
from ......special_exception import HTTPException
from fastapi import (
    Header
)
from fastapi.responses import ORJSONResponse
from ._warnings import WARNINGS
from ._request import RaiseWarningRequest
from ..._admin_router import admin_router

@admin_router.post("/debug/raise_warning")
async def raise_warning_api(
    request: RaiseWarningRequest,
):
    """
    This API is used to collapse the server.
    """
    if request.type not in WARNINGS:
        raise HTTPException(detail="Invalid warning type", status_code=400)
    
    warning = WARNINGS[request.type]

    warnings.warn(
        request.message,
        category=warning,
    )

    return ORJSONResponse(
        {
            "warning": str(warning),
            "message": request.message
        }
    )
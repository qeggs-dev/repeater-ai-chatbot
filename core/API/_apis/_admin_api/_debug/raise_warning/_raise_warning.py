import warnings
from ....._server import Server
from fastapi import (
    HTTPException,
    Header
)
from fastapi.responses import ORJSONResponse
from ._warnings import WARNINGS
from ._request import RaiseWarningRequest

@Server.app.post("/admin/debug/raise_warning")
async def raise_warning_api(
        request: RaiseWarningRequest,
        api_key: str = Header(..., alias="X-Admin-API-Key")
    ):
    """
    This API is used to collapse the server.
    """
    if not Server.admin_key_manager.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    
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
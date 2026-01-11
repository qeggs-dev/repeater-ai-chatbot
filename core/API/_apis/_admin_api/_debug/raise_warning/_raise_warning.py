import warnings
from ....._resource import Resource
from fastapi import (
    HTTPException,
    Header
)
from fastapi.responses import ORJSONResponse
from ._warnings import WARNINGS
from ._request import RaiseWarningRequest

@Resource.app.post("/admin/debug/raise_warning")
async def raise_warning_api(
        request: RaiseWarningRequest,
        api_key: str = Header(..., alias="X-Admin-API-Key")
    ):
    """
    This API is used to collapse the server.
    """
    if not Resource.admin_key_manager.validate_key(api_key):
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
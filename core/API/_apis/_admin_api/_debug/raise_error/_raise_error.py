from typing import NoReturn
from ....._resource import Resource
from fastapi import (
    HTTPException,
    Header
)
from ._errors import ERRORS
from ._request import RaiseErrorRequest

@Resource.app.post("/admin/debug/raise_error")
async def raise_error_api(
        request: RaiseErrorRequest,
        api_key: str = Header(..., alias="X-Admin-API-Key")
    ):
    """
    This API is used to collapse the server.
    """
    if not Resource.admin_key_manager.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    
    if request.type not in ERRORS:
        raise HTTPException(detail="Invalid error type", status_code=400)
    
    raise ERRORS[request.type](*request.args, **request.kwargs)
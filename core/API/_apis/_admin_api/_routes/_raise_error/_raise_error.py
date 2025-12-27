from typing import NoReturn
from ....._resource import (
    app,
    admin_api_key,
)
from fastapi import (
    HTTPException,
    Header
)
from ._errors import ERRORS
from ._request import RaiseErrorRequest

@app.post("/admin/raise_error")
async def raise_error(
        request: RaiseErrorRequest,
        api_key: str = Header(..., alias="X-Admin-API-Key")
    ) -> NoReturn:
    """
    This API is used to collapse the server.
    """
    if not admin_api_key.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    
    if request.error_type not in ERRORS:
        raise HTTPException(detail="Invalid error type", status_code=400)
    
    raise ERRORS[request.error_type](*request.error_args, **request.error_kwargs)
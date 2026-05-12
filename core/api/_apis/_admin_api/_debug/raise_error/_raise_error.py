from ......special_exception import HTTPException
from ._errors import ERRORS
from ._request import RaiseErrorRequest
from ..._admin_router import admin_router

@admin_router.post("/debug/raise_error")
async def raise_error_api(
    request: RaiseErrorRequest
):
    """
    This API is used to collapse the server.
    """
    if request.type not in ERRORS:
        raise HTTPException(detail="Invalid error type", status_code=400)
    
    raise ERRORS[request.type](*request.args, **request.kwargs)
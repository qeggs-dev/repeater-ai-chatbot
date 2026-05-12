from fastapi import APIRouter, Depends, Request
from ....server import RepeaterMain
from ....special_exception import HTTPException

def check_admin_api_key(request: Request):
    api_key = request.headers.get("X-Admin-API-Key")
    server = RepeaterMain.get_now_server()
    if api_key is None:
        raise HTTPException(detail="API key is required", status_code=401)
    elif not server.admin_key_manager.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    
    return api_key

admin_router = APIRouter(prefix = "/admin", tags=["admin"], dependencies=[Depends(check_admin_api_key)])
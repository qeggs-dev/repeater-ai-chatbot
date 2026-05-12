from .._root import root_router
from ._router import request_log_router

root_router.include_router(request_log_router)
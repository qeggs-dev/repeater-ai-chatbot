from .._root import root_router
from ._router import status_router

root_router.include_router(status_router)
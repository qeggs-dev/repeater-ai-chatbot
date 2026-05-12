from .._root import root_router
from ._router import web_router

root_router.include_router(web_router)
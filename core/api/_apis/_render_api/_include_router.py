from .._root import root_router
from ._router import render_router

root_router.include_router(render_router)
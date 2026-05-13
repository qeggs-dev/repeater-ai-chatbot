from .._root import root_router
from ._router import static_router

root_router.include_router(static_router)
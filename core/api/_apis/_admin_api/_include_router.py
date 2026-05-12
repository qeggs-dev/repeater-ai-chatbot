
from .._root import root_router
from ._admin_router import admin_router

root_router.include_router(admin_router)
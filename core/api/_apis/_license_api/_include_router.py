from .._root import root_router
from ._router import license_router

root_router.include_router(license_router)
from .._root import root_router
from ._router import ping_provider_router

root_router.include_router(ping_provider_router)
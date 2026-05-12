from ..._root import root_router
from ._router import nexus_router

root_router.include_router(nexus_router)
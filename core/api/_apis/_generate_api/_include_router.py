from .._root import root_router
from ._router import generate_router

root_router.include_router(generate_router)
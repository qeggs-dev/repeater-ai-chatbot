from .._root import root_router
from ._router import template_router

root_router.include_router(template_router)
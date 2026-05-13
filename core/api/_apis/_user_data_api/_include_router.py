from .._root import root_router
from ._router import user_data_router

root_router.include_router(user_data_router)
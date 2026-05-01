from .._router import user_data_router
from ._router import context_router

user_data_router.include_router(context_router)
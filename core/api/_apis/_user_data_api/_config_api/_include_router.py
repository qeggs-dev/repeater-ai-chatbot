from .._router import user_data_router
from ._router import config_router

user_data_router.include_router(config_router)
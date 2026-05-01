from .._router import user_data_router
from ._router import merged_user_data_router

user_data_router.include_router(merged_user_data_router)
from .._router import user_data_router
from ._router import user_file_router

user_data_router.include_router(user_file_router)
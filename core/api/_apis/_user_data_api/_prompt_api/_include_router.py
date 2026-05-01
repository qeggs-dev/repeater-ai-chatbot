from .._router import user_data_router
from ._router import prompt_router

user_data_router.include_router(prompt_router)
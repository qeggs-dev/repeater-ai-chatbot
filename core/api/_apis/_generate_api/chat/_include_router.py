from .._router import generate_router
from ._router import chat_router

generate_router.include_router(chat_router)
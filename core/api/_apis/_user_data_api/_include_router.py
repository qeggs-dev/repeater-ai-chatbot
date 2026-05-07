from ....server import Server
from ._router import user_data_router

Server.app.include_router(user_data_router)
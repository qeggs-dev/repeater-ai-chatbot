from ....server import Server
from ._router import request_log_router

Server.app.include_router(request_log_router)
from ....server import Server
from ._router import status_router

Server.app.include_router(status_router)
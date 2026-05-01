from ....server import Server
from ._router import static_router

Server.app.include_router(static_router)
from ....server import Server
from ._router import web_router

Server.app.include_router(web_router)
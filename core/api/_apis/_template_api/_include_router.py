from ....server import Server
from ._router import template_router

Server.app.include_router(template_router)
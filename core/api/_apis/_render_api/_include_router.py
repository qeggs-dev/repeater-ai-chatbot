from ....server import Server
from ._router import render_router

Server.app.include_router(render_router)
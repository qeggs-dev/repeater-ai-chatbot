from ....server import Server
from ._router import generate_router

Server.app.include_router(generate_router)
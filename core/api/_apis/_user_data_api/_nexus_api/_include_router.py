from .....server import Server
from ._router import nexus_router

Server.app.include_router(nexus_router)
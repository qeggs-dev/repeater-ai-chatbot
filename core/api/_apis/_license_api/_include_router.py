from ....server import Server
from ._router import license_router

Server.app.include_router(license_router)
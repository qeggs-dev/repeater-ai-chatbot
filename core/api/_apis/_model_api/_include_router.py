from ....server import Server
from ._router import models_router

Server.app.include_router(models_router)
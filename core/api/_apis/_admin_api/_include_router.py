
from ....server import Server
from ._admin_router import admin_router

Server.app.include_router(admin_router) # add router to app
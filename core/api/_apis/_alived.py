from ...server import Server
from fastapi.responses import PlainTextResponse

@Server.app.get("/alived", tags=["alived_check"])
def alived():
    return PlainTextResponse("OK")
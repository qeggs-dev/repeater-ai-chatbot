from ._root import root_router
from fastapi.responses import PlainTextResponse

@root_router.get("/alived", tags=["alived_check"])
def alived():
    return PlainTextResponse("OK")
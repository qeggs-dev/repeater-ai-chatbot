from .._resource import Resource
from fastapi.responses import PlainTextResponse

@Resource.app.get("/alived")
def test_alived():
    return PlainTextResponse("OK")
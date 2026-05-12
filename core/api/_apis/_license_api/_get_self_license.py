from ....server import RepeaterMain
from ._router import license_router
from fastapi.responses import ORJSONResponse

@license_router.get("/self")
async def get_license():
    """
    Get license information
    """
    server = RepeaterMain.get_now_server()
    return ORJSONResponse(
        await server.core.runtime.licenses.get_self_license(),
    )
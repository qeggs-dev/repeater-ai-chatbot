from ....server import Server
from ._router import license_router
from fastapi.responses import ORJSONResponse

@license_router.get("/self")
async def get_license():
    """
    Get license information
    """
    return ORJSONResponse(
        await Server.core.runtime.licenses.get_self_license(),
    )
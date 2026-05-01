from ....server import Server
from ._router import license_router
from fastapi.responses import ORJSONResponse, PlainTextResponse

@license_router.get("/requirement_list")
async def get_requirement_list():
    """
    Get license information
    """
    return ORJSONResponse(
        Server.core.runtime.licenses.get_requirements_list(),
    )
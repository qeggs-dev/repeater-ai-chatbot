from ....server import RepeaterMain
from ._router import license_router
from fastapi.responses import ORJSONResponse, PlainTextResponse

@license_router.get("/requirement/{requirement_name}")
async def get_requirement_license(requirement_name: str):
    """
    Get license information
    """
    server = RepeaterMain.get_now_server()
    if requirement_name not in server.core.runtime.licenses:
        return PlainTextResponse(
            "Requirement name not found",
            status_code=404
        )
            
    return ORJSONResponse(
        await server.core.runtime.licenses.get_requirement_license(requirement_name)
    )
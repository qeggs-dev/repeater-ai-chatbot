from ....repeater_main import RepeaterMain
from ._router import license_router
from fastapi.responses import ORJSONResponse

@license_router.get("/requirement_list")
async def get_requirement_list():
    """
    Get license information
    """
    server = RepeaterMain.get_now_server()
    return ORJSONResponse(
        server.runtime.licenses.get_requirements_list(),
    )
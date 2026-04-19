from ....server import Server
from fastapi.responses import ORJSONResponse, PlainTextResponse

@Server.app.get("/license/requirement_list")
async def get_requirement_list():
    """
    Get license information
    """
    return ORJSONResponse(
        Server.licenses.get_requirements_list(),
    )
from ....server import Server
from fastapi.responses import ORJSONResponse, PlainTextResponse
from ....runtime_container import RuntimeContainer

@Server.app.get("/license/requirement_list")
async def get_requirement_list():
    """
    Get license information
    """
    return ORJSONResponse(
        RuntimeContainer.get_runtime().licenses.get_requirements_list(),
    )
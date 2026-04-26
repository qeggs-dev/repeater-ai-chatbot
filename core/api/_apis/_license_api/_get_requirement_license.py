from ....server import Server
from fastapi.responses import ORJSONResponse, PlainTextResponse
from ....runtime_container import RuntimeContainer

@Server.app.get("/license/requirement/{requirement_name}")
async def get_requirement_license(requirement_name: str):
    """
    Get license information
    """
    if requirement_name not in RuntimeContainer.get_runtime().licenses:
        return PlainTextResponse(
            "Requirement name not found",
            status_code=404
        )
            
    return ORJSONResponse(
        await RuntimeContainer.get_runtime().licenses.get_requirement_license(requirement_name)
    )
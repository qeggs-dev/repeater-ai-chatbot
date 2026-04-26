from ....server import Server
from fastapi.responses import ORJSONResponse, PlainTextResponse

@Server.app.get("/license/requirement/{requirement_name}")
async def get_requirement_license(requirement_name: str):
    """
    Get license information
    """
    if requirement_name not in Server.core.runtime.licenses:
        return PlainTextResponse(
            "Requirement name not found",
            status_code=404
        )
            
    return ORJSONResponse(
        await Server.core.runtime.licenses.get_requirement_license(requirement_name)
    )
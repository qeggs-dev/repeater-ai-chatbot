from ..._resource import Resource
from fastapi.responses import ORJSONResponse, PlainTextResponse

@Resource.app.get("/license/requirement/{requirement_name}")
async def get_requirement_license(requirement_name: str):
    """
    Get license information
    """
    if requirement_name not in Resource.licenses:
        return PlainTextResponse(
            "Requirement name not found",
            status_code=404
        )
            
    return ORJSONResponse(
        await Resource.licenses.get_requirement_license(requirement_name)
    )
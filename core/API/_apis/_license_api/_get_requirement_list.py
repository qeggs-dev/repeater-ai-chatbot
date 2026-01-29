from ..._resource import Resource
from fastapi.responses import ORJSONResponse, PlainTextResponse

@Resource.app.get("/license/requirement_list")
async def get_requirement_list():
    """
    Get license information
    """
    return ORJSONResponse(
        Resource.licenses.get_requirements_list(),
    )
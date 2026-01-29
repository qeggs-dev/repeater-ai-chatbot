from ..._resource import Resource
from fastapi.responses import ORJSONResponse

@Resource.app.get("/license/self")
async def get_license():
    """
    Get license information
    """
    return ORJSONResponse(
        await Resource.licenses.get_self_license(),
    )
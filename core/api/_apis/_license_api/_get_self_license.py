from ....server import Server
from fastapi.responses import ORJSONResponse

@Server.app.get("/license/self")
async def get_license():
    """
    Get license information
    """
    return ORJSONResponse(
        await Server.licenses.get_self_license(),
    )
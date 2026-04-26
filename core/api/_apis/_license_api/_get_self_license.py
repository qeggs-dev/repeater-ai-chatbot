from ....server import Server
from fastapi.responses import ORJSONResponse
from ....runtime_container import RuntimeContainer

@Server.app.get("/license/self")
async def get_license():
    """
    Get license information
    """
    return ORJSONResponse(
        await RuntimeContainer.get_runtime().licenses.get_self_license(),
    )
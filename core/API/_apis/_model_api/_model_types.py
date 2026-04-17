from ....server import Server
from ....model_api import ModelType
from fastapi.responses import ORJSONResponse
from ._resources import MODEL_TYPES

@Server.app.get("/model/types")
async def model_types():
    """Get all model types"""
    return ORJSONResponse(
        MODEL_TYPES
    )
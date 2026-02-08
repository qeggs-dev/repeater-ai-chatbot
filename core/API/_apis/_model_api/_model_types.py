from ..._resource import Resource
from ....Model_API import ModelType
from fastapi.responses import ORJSONResponse
from ._resources import MODEL_TYPES

@Resource.app.get("/model/types")
async def model_types():
    """Get all model types"""
    return ORJSONResponse(
        MODEL_TYPES
    )
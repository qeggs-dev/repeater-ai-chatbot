from ..._resource import Resource
from ....Model_API import ModelType
from fastapi.responses import ORJSONResponse
from fastapi import HTTPException
from ._resources import MODEL_TYPES

@Resource.app.get("/model/list/{model_type}")
async def model_list(model_type: str):
    if model_type not in MODEL_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid model type."
        )
    model_list = Resource.core.model_api_manager.model_list(
        ModelType(model_type)
    )

    return ORJSONResponse(
        status_code = 200,
        content = [model.model_dump() for model in model_list]
    )
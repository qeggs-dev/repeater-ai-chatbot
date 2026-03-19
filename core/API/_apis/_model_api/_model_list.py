from ..._resource import Resource
from ....Model_API import ModelType, ModelsResponse, ExceptionResponse
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
    model_info = await Resource.core.model_api_manager.get_models(
        ModelType(model_type)
    )

    if isinstance(model_info, ExceptionResponse):
        return ORJSONResponse(
            status_code = 503,
            content = model_info.model_dump()
        )
    return ORJSONResponse(
        status_code = 200,
        content = model_info.model_dump()
    )
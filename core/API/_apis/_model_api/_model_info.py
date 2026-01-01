from ..._resource import app, chat
from ....ApiInfo import ModelType
from fastapi.responses import ORJSONResponse
from fastapi import HTTPException
from ._resources import MODEL_TYPES

@app.get("/model/info/{model_type}/{model_uid}")
async def model_info(model_type: str, model_uid: str):
    if model_type not in MODEL_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid model type."
        )
    model_list = chat.apiinfo.find(
        ModelType(model_type),
        model_uid
    )

    return ORJSONResponse(
        status_code = 200,
        content=[model.model_dump() for model in model_list]
    )
from ..._resource import app, chat
from ....ApiInfo import ModelType
from fastapi.responses import ORJSONResponse

MODEL_TYPES = [t.value for t in ModelType]

@app.get("/model/list/{model_type}")
async def model_list(model_type: str):
    if model_type not in MODEL_TYPES:
        return ORJSONResponse(
            status_code=400,
            content={
                "message": "Invalid model type",
                "data": []
            }
        )
    chat_api_list = chat.apiinfo.uid_list(
        ModelType(model_type)
    )

    return ORJSONResponse(
        status_code=200,
        content={
            "message": "Success",
            "data": chat_api_list
        }
    )
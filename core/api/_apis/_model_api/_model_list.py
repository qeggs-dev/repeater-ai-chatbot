from ....server import Server
from ._router import models_router
from fastapi.responses import ORJSONResponse
from ....special_exception import HTTPException
from ._response import ResponseModel

@models_router.get("/")
async def model_list():
    response = await Server.core.runtime.model_api_manager.get_all_models()
    if response.code == 200:
        model_info = response.get_data()
        if model_info is None:
            raise HTTPException(
                status_code = 500,
                detail = "Model INFO Server Response is invalid."
            )
        models = [model.to_safe() for model in model_info.models]
        return ORJSONResponse(
            status_code = 200,
            content = ResponseModel(
                message = model_info.message,
                models = models
            ).model_dump(exclude_none=True)
        )
    else:
        raise HTTPException(
            status_code = 500,
            detail = response.text
        )
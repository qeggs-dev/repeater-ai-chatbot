# ==== 标准库 ==== #
import random

# ==== 第三方库 ==== #
from loguru import logger

# ==== 自定义库 ==== #
from ..user_config_manager import (
    UserConfigs
)
from ..global_config_manager import GlobalConfigs
from ..special_exception import HTTPException
from ..clients.model_info import (
    ModelsClient,
    ModelInfo,
)

async def get_model(
    model_id: str | list[str] | None,
    model_info_client: ModelsClient,
) -> ModelInfo:
    if model_id is None:
        raise HTTPException(
            status_code = 400,
            detail = "Model ID is required"
        )
    
    if isinstance(model_id, str):
        model_id = [model_id]
    
    models: list[ModelInfo] = []
    for id in model_id:
        # 获取API信息
        model_info_response = await model_info_client.get_models(id)
        if model_info_response.code != 200:
            raise HTTPException(
                status_code = model_info_response.code,
                detail = f"Model Info Server Error: {model_info_response.text}",
            )
        model_info = model_info_response.get_data()
        models.extend(model_info.models)
        if model_info.models:
            break
    
    if models is None:
        raise HTTPException(
            status_code = 404,
            detail = "Error: Model Info Server Response is Empty.",
        )
    
    models = model_info.models
    if not models:
        raise HTTPException(
            status_code = 404,
            detail = "Error: Model is Not Found.",
        )
    
    model = random.choice(models)

    return model
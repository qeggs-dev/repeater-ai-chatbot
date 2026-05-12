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
    model_uid: str | list[str] | None,
    model_info_client: ModelsClient,
) -> ModelInfo:
    
    # 如果有多个，则随机选择一个
    if isinstance(model_uid, list):
        if len(model_uid) == 1:
            model_uid_str = model_uid[0]
        elif len(model_uid) > 1:
            model_uid_str = random.choice(model_uid)
        else:
            raise HTTPException(
                status_code = 500,
                detail = "Error: No model uid is specified.",
            )
    elif isinstance(model_uid, str):
        model_uid_str = model_uid
    else:
        raise HTTPException(
            status_code = 500,
            detail = "Error: Model uid must be a string or a list of strings.",
        )
    
    # 获取API信息
    model_info_response = await model_info_client.get_models(model_uid_str)
    if model_info_response.code != 200:
        raise HTTPException(
            status_code = model_info_response.code,
            detail = f"Model Info Server Error: {model_info_response.text}",
        )
    model_info = model_info_response.get_data()
    if not model_info:
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
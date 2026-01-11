from ...._resource import Resource
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger

@Resource.app.get("/userdata/config/get/{user_id}")
async def get_config(user_id: str):
    """
    Endpoint for get config
    """
    # 获取用户ID为user_id的配置
    config = await Resource.core.get_config(user_id = user_id)
    
    logger.info(f"Get user config", user_id = user_id)

    # 返回配置
    return ORJSONResponse(config.model_dump(exclude_none=True))
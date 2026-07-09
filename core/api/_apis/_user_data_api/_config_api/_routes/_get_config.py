from ......repeater_main import RepeaterMain
from .._router import config_router
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger

@config_router.get("/get/{user_id}")
@config_router.get("/get/{user_id}.json")
async def get_config(user_id: str):
    """
    Endpoint for get config
    """
    server = RepeaterMain.get_now_server()

    # 获取用户ID为user_id的配置
    config = await server.core.get_config(user_id = user_id)
    
    logger.info(
        "Get user config",
        user_id = user_id
    )

    # 返回配置
    return ORJSONResponse(config.model_dump(exclude_none=True))
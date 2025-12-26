from ...._resource import (
    chat,
    app
)
from fastapi.responses import (
    ORJSONResponse,
    PlainTextResponse
)
from fastapi import (
    Form
)
from loguru import logger

@app.get("/userdata/config/branchs/{user_id}")
async def get_config_branch_id(user_id: str):
    """
    Endpoint for get config branch id

    Args:
        user_id (str): The user id
    
    Returns:
        ORJSONResponse: Current user's branch list
    """

    # 获取平行配置路由ID列表
    branchs = await chat.user_config_manager.get_all_item_id(user_id)

    logger.info(f"Get user branchs list", user_id = user_id)

    # 返回分支ID列表
    return ORJSONResponse(branchs)

@app.get("/userdata/config/now_branch/{user_id}")
async def get_config_now_branch_id(user_id: str):
    """
    Endpoint for get config branch id

    Args:
        user_id (str): User id

    Returns:
        PlainTextResponse: Now Branch id
    """

    # 获取当前配置路由ID
    branch_id = await chat.user_config_manager.get_default_item_id(user_id)

    logger.info(f"Get user now branch id", user_id = user_id)

    # 返回分支ID
    return PlainTextResponse(branch_id)

@app.put("/userdata/config/change/{user_id}")
async def change_config(user_id: str, new_branch_id: str = Form(...)):
    """
    Endpoint for changing config

    Args:
        user_id (str): User id
        new_branch_id (str): New branch id
    
    Returns:
        PlainTextResponse: Plain text response
    """

    # 设置平行配置路由
    await chat.user_config_manager.set_default_item_id(user_id, item = new_branch_id)

    logger.info("Change user config branch id to {new_branch_id}", user_id = user_id, new_branch_id = new_branch_id)

    # 返回成功文本
    return PlainTextResponse("Config branch changed")
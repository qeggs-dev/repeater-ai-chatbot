from ..._resource import Resource
from fastapi import Form
from fastapi.responses import (
    ORJSONResponse,
    PlainTextResponse
)
from loguru import logger

@Resource.app.get("/userdata/prompt/branchs/{user_id}")
async def get_prompt_branch_id_list(user_id: str):
    """
    Endpoint for getting prompt branch ID

    Args:
        user_id (str): User ID

    Returns:
        ORJSONResponse: Prompt branch ID
    """
    # 获取用户ID为user_id的提示词分支ID
    branchs = await Resource.core.prompt_manager.get_all_branch_id(user_id)

    logger.info("Get prompt branch", user_id=user_id)

    # 返回分支ID
    return ORJSONResponse(branchs)

@Resource.app.get("/userdata/prompt/now_branch/{user_id}")
async def get_prompt_now_branch_id(user_id: str):
    """
    Endpoint for getting prompt branch ID

    Args:
        user_id (str): User ID

    Returns:
        PlainTextResponse: Now Branch ID
    """
    # 获取用户ID为user_id的提示词分支ID
    branch_id = await Resource.core.prompt_manager.get_default_branch_id(user_id)

    logger.info("Get prompt branch", user_id=user_id)

    # 返回分支ID
    return PlainTextResponse(branch_id)

@Resource.app.put("/userdata/prompt/change/{user_id}")
async def change_prompt(user_id: str, new_branch_id: str = Form(...)):
    """
    Endpoint for changing prompt

    Args:
        user_id (str): User ID
        new_branch_id (str): New prompt ID
    
    Returns:
        PlainTextResponse: Success text for successful change
    """

    # 设置用户ID为user_id的提示词为new_prompt_id
    await Resource.core.prompt_manager.set_default_branch_id(user_id, branch_id = new_branch_id)

    logger.info("Change prompt to {new_branch_id}", user_id=user_id, new_branch_id=new_branch_id)

    # 返回成功文本
    return PlainTextResponse("Prompt branch changed")
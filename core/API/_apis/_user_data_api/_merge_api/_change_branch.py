from ...._resource import Resource
from fastapi import Form
from fastapi.responses import (
    PlainTextResponse
)
from loguru import logger
from .._user_data_type import UserDataType, get_manager

@Resource.app.put("/userdata/{user_data_type}/change/{user_id}")
async def change_branch(user_data_type: UserDataType, user_id: str, new_branch_id: str = Form(...)):
    """
    Endpoint for changing branch

    Args:
        user_id (str): User ID
        new_branch_id (str): New branch ID
    
    Returns:
        PlainTextResponse: Success text for successful change
    """

    # 设置用户ID为user_id的提示词为new_prompt_id
    manager = get_manager(user_data_type)
    manager.set_active_branch_id(user_id, branch_id = new_branch_id)

    logger.info(
        "Change {user_data_type} branch to {new_branch_id}",
        user_id = user_id,
        new_branch_id = new_branch_id,
        user_data_type = user_data_type.value
    )

    # 返回成功文本
    return PlainTextResponse("Branch changed")
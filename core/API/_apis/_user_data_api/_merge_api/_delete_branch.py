from ...._resource import Resource
from fastapi.responses import (
    PlainTextResponse
)
from .._user_data_type import UserDataType, get_manager
from loguru import logger

@Resource.app.delete("/userdata/{user_data_type}/delete/{user_id}")
async def delete_branch(user_data_type: UserDataType, user_id: str):
    """
    Endpoint for deleting

    Args:
        user_id (str): User ID

    Returns:
        PlainTextResponse: Success text for successful deletion
    """
    manager = get_manager(user_data_type)

    # 删除用户ID为user_id的提示词
    await manager.delete(user_id)

    logger.info(
        "Delete {user_data_type} active branch",
        user_id = user_id,
        user_data_type = user_data_type.value
    )

    # 返回成功文本
    return PlainTextResponse("Branch deleted")
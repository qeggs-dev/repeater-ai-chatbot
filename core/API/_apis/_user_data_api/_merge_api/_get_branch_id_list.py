from ...._resource import Resource
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger
from .._user_data_type import UserDataType, get_manager

@Resource.app.get("/userdata/{user_data_type}/branchs/{user_id}")
async def get_branch_id_list(user_data_type: UserDataType, user_id: str):
    """
    Endpoint for getting branch ID

    Args:
        user_id (str): User ID

    Returns:
        ORJSONResponse: Branch ID
    """
    manager = get_manager(user_data_type)

    branchs = await manager.get_all_branch_id(user_id)

    logger.info(
        "Get {user_data_type} branchs list",
        user_id = user_id,
        user_data_type = user_data_type.value
    )

    # 返回分支ID
    return ORJSONResponse(branchs)
from .._router import merged_user_data_router
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger
from ..._user_data_type import UserDataType, get_manager

@merged_user_data_router.get("/{user_data_type}/info/{user_id}")
async def get_branch_info(user_data_type: UserDataType, user_id: str):
    """
    Get branch info

    Args:
        user_id (str): user id
    """
    manager = get_manager(user_data_type)
    info = await manager.info(user_id)

    logger.info(
        "Get {user_data_type} active branch info",
        user_id = user_id,
        user_data_type = user_data_type.value
    )

    return ORJSONResponse(
        content = info.model_dump()
    )
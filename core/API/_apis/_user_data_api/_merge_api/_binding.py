from ...._resource import Resource
from fastapi.responses import (
    ORJSONResponse
)
from fastapi import (
    Form
)
from loguru import logger
from .._user_data_type import UserDataType, get_manager

@Resource.app.put("/userdata/{user_data_type}/binding/{user_id}")
async def binding_branch(user_data_type: UserDataType, user_id: str, dst_branch_id: str = Form(...)):
    """
    Binding branch

    Args:
        user_id (str): User ID
        dst_branch_id (str): Destination branch ID
    """
    manager = get_manager(user_data_type)
    await manager.binding(user_id, dst_branch_id)

    logger.info(
        "Binding {user_data_type} branch from active branch to {branch_id}",
        user_id = user_id,
        branch_id = dst_branch_id,
        user_data_type = user_data_type.value
    )

    return ORJSONResponse({"status": "success"})


@Resource.app.put("/userdata/{user_data_type}/binding_from/{user_id}")
async def binding_branch_from(user_data_type: UserDataType, user_id: str, src_branch_id: str = Form(...)):
    """
    Binding branch from another branch

    Args:
        user_id (str): User ID
        src_branch_id (str): Source branch ID
    """
    manager = get_manager(user_data_type)
    await manager.binding_from(user_id, src_branch_id)

    logger.info(
        "Binding {user_data_type} branch from {branch_id} to active branch",
        user_id = user_id,
        branch_id = src_branch_id,
        user_data_type = user_data_type.value
    )

    return ORJSONResponse({"status": "success"})
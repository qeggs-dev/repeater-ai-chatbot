from ....._resource import Resource
from fastapi.responses import (
    ORJSONResponse
)
from fastapi import (
    Form
)

@Resource.app.put("/userdata/config/binding/{user_id}")
async def binding_branch(user_id: str, dst_branch_id: str = Form(...)):
    """
    Binding branch

    Args:
        user_id (str): User ID
        dst_branch_id (str): Destination branch ID
    """
    manager = Resource.core.user_config_manager
    await manager.binding(user_id, dst_branch_id)

    return ORJSONResponse({"status": "success"})


@Resource.app.put("/userdata/config/binding_from/{user_id}")
async def binding_branch_from(user_id: str, src_branch_id: str = Form(...)):
    """
    Binding branch from another branch

    Args:
        user_id (str): User ID
        src_branch_id (str): Source branch ID
    """
    manager = Resource.core.user_config_manager
    await manager.binding_from(user_id, src_branch_id)

    return ORJSONResponse({"status": "success"})
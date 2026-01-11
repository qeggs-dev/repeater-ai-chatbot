from ....._resource import Resource
from fastapi.responses import (
    ORJSONResponse
)
from fastapi import (
    Form
)

@Resource.app.put("/userdata/config/clone/{user_id}")
async def clone_branch(user_id: str, dst_branch_id: str = Form(...)):
    """
    Cloning branch

    Args:
        user_id (str): User ID
        dst_branch_id (str): Destination branch ID
    """
    manager = Resource.core.user_config_manager
    await manager.clone(user_id, dst_branch_id)

    return ORJSONResponse({"status": "success"})


@Resource.app.put("/userdata/config/clone_from/{user_id}")
async def clone_branch_from(user_id: str, src_branch_id: str = Form(...)):
    """
    Cloning branch from another branch

    Args:
        user_id (str): User ID
        src_branch_id (str): Source branch ID
    """
    manager = Resource.core.user_config_manager
    await manager.clone_from(user_id, src_branch_id)

    return ORJSONResponse({"status": "success"})
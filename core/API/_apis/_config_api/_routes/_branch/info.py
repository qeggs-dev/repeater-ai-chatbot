from ....._resource import Resource
from fastapi.responses import (
    ORJSONResponse
)
from fastapi import (
    Form
)

@Resource.app.get("/userdata/config/info/{user_id}")
async def get_branch_info(user_id: str):
    """
    Get branch info

    Args:
        user_id (str): user id
    """
    manager = Resource.core.user_config_manager
    info = await manager.info(user_id)

    return ORJSONResponse(
        content = info.model_dump()
    )
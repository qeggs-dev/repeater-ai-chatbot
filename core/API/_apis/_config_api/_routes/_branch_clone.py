from ...._resource import Resource
from fastapi.responses import (
    ORJSONResponse,
    PlainTextResponse
)
from fastapi import (
    Form
)
from loguru import logger

@Resource.app.put("/userdata/config/clone/{user_id}")
async def clone_branch(user_id: str, dst_branch_id: str = Form(...)):
    """
    Cloning branch

    Args:
        user_id (str): User ID
        dst_branch_id (str): Destination branch ID
    """
    manager = Resource.core.user_config_manager
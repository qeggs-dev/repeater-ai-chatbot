from ......server import Server
from ......context_manager import (
    ContentRole
)
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger

@Server.app.post("/userdata/context/role_mapping/{user_id}")
async def role_mapping(user_id: str, role_map: dict[ContentRole, ContentRole | None]):
    """
    Context role mapping endpoint.

    Args:
        user_id (str): The ID of the user.
        role_map (dict[ContentRole, ContentRole | None]): The role mapping to apply.

    Returns:
        ORJSONResponse: A response indicating the success or failure of the operation.
    """
    context_loader = await Server.core.get_context_loader()
    context = await context_loader.load_context(user_id)

    context.role_map(role_map)
    await context_loader.save(user_id, context)
    logger.info(f"User {user_id} injected context")
    return ORJSONResponse(
        {
            "status": "success",
            "context": context.context
        }
    )
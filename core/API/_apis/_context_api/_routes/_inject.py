from ...._resource import (
    chat,
    app
)
from .....Context_Manager import (
    ContentUnit,
    ContentRole
)
from fastapi.responses import (
    ORJSONResponse
)
from loguru import logger

@app.post("/userdata/context/inject/{user_id}")
async def inject_context(user_id: str, request: ContentUnit):
    """
    注入上下文
    """
    context_loader = await chat.get_context_loader()
    context = await context_loader.get_context_object(user_id)

    context.append(
        ContentUnit(
            role = ContentRole.USER,
            content = request.user_content,
        )
    )
    context.append(
        ContentUnit(
            role = ContentRole.ASSISTANT,
            content = request.assistant_content,
        )
    )
    await context_loader.save(user_id, context)
    logger.info(f"User {user_id} injected context")
    return ORJSONResponse(
        {
            "status": "success",
            "context": context.context
        }
    )
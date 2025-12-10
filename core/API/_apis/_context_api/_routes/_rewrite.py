from ...._resource import (
    chat,
    app
)
from fastapi.responses import (
    ORJSONResponse
)
from fastapi import HTTPException
from loguru import logger

from .._requests import (
    RewriteContext
)

@app.post("/userdata/context/rewrite/{user_id}")
async def rewrite_context(user_id: str, rewrite_context: RewriteContext):
    """
    Endpoint for rewriting context

    Args:
        user_id (str): User ID
        rewrite_context (RewriteContext): Context to rewrite

    Returns:
        ORJSONResponse: New context
    """
    # 从context_loader中加载用户ID为user_id的上下文
    context_loader = await chat.get_context_loader()
    context = await context_loader.get_context_object(user_id)

    # 检查索引是否在上下文范围内
    if 0 <= rewrite_context.index < len(context.context_list):
        if rewrite_context.content:
            context.context_list[rewrite_context.index].content = rewrite_context.content
        if rewrite_context.reasoning_content:
            if context.context_list[rewrite_context.index].role == "assistant":
                context.context_list[rewrite_context.index].reasoning_content = rewrite_context.reasoning_content
            else:
                raise HTTPException(400, "Only assistant can have reasoning_content")
        await context_loader.save(user_id, context)
    else:
        raise HTTPException(400, "Index out of range")
    
    logger.info(f"Rewrite {rewrite_context.index} Context", user_id = user_id)
    
    # 返回ORJSONResponse，新的上下文内容
    return ORJSONResponse(context)
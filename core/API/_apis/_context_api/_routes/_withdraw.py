from ...._resource import (
    chat,
    app
)
from .....Context_Manager import (
    ContextObject
)
from fastapi import Form
from fastapi.responses import (
    ORJSONResponse
)
from fastapi import HTTPException
from loguru import logger

@app.post("/userdata/context/withdraw/{user_id}")
async def withdraw_context(user_id: str, context_pair_num: int = Form(1, gt=0)):
    """
    Endpoint for withdrawing context

    Args:
        user_id (str): The user ID
        length (int | None): The number of messages to withdraw

    Returns:
        ORJSONResponse: New context
    """
    # 从context_loader中加载用户ID为user_id的上下文
    context_loader = await chat.get_context_loader()
    context = await context_loader.load_context(user_id)
    pop_items: list[ContextObject] = []
    
    try:
        for _ in range(context_pair_num):
            pop_items.append(
                context.withdraw()
            )
    except (ValueError, IndexError) as e:
        raise HTTPException(400, str(e)) from e
    
    pop_context = ContextObject()
    for item in pop_items[::-1]:
        pop_context.context_list.extend(
            item.context_list
        )
    
    # 返回ORJSONResponse，新的上下文内容
    await context_loader.save(user_id, context)
    logger.info(f"User {user_id} withdraw {len(pop_context)} context pairs")
    return ORJSONResponse(
        {
            "status": "success",
            "deleted": len(pop_context),
            "deleted_context": pop_context.context,
            "delete_context_pair": len(pop_items),
            "context": context.context,
        }
    )
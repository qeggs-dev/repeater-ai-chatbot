from ...._resource import (
    chat,
    app
)
from fastapi import Form
from fastapi.responses import (
    PlainTextResponse
)
from loguru import logger

@app.get("/userdata/context/branchs/{user_id}")
async def get_context_branch_id_list(user_id: str):
    """
    Endpoint for getting context branch id list

    Args:
        user_id (str): User ID

    Returns:
        ORJSONResponse: Context branch id list
    """
    return chat.context_manager.get_all_branch_id(user_id)

@app.get("/userdata/context/now_branch/{user_id}")
async def get_context_now_branch_id(user_id: str):
    """
    Endpoint for getting context branch id

    Args:
        user_id (str): User ID

    Returns:
        ORJSONResponse: Context branch id
    """
    # 获取用户ID为user_id的上下文分支ID
    branch_id = await chat.context_manager.get_default_branch_id(user_id)

    logger.info(f"Get Context branch id", user_id = user_id)

    # 返回上下文分支ID
    return PlainTextResponse(branch_id)

@app.put("/userdata/context/change/{user_id}")
async def change_context(user_id: str, new_branch_id: str = Form(...)):
    """
    Endpoint for changing context

    Args:
        user_id (str): User ID
        new_branch_id (str): New context branch ID
    
    Returns:
        PlainTextResponse: Success text for changing context
    """

    # 设置用户ID为user_id的上下文为new_context_id
    await chat.context_manager.set_default_branch_id(user_id, branch_name = new_branch_id)

    logger.info("Change Context to {new_branch_id}", user_id = user_id, new_branch_id = new_branch_id)

    # 返回成功文本
    return PlainTextResponse("Context changed successfully")
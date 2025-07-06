import orjson
from environs import Env
env = Env()
env.read_env()
from fastapi import (
    FastAPI,
    Request,
    BackgroundTasks,
    Form,
    Query,
    Header
)
from fastapi.responses import (
    FileResponse,
    JSONResponse,
    PlainTextResponse,
    StreamingResponse
)
from fastapi.exceptions import (
    HTTPException
)
from loguru import logger
from .._resource import app, chat, core

@app.post("/chat/completion/{user_id}")
async def chat_endpoint(
    user_id: str,
    message: str = Form(""),
    user_name: str = Form(""),
    role: str = Form("user"),
    role_name: str = Form(None),
    model_type: str | None = Form(None),
    load_prompt: bool = Form(True),
    save_context: bool = Form(True),
    reference_context_id: str | None = Form(None),
    continue_completion: bool = Form(False)
):
    """
    Endpoint for chat
    """
    if continue_completion and message:
        raise HTTPException(detail="Cannot send message when continuing completion", status_code=400)
    try:
        context = await chat.Chat(
            user_id = user_id,
            message = message,
            user_name = user_name,
            role = role,
            role_name = role_name,
            model_type = model_type,
            print_chunk = True,
            load_prompt = load_prompt,
            save_context = save_context,
            reference_context_id = reference_context_id,
            continue_completion = continue_completion
        )
    except core.ApiInfo.APIGroupNotFoundError as e:
        raise HTTPException(detail=str(e), status_code=400)
    return JSONResponse(context)
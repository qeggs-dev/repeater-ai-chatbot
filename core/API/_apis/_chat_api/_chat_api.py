import orjson
import asyncio

from typing import AsyncIterator
from environs import Env
env = Env()
env.read_env()
from fastapi.responses import (
    ORJSONResponse,
    StreamingResponse
)
from ....SpecialException import (
    HTTPException
)
from ..._resource import Resource
from ....Assist_Struct import Response
from ....CallAPI import CompletionsAPI

from ._requests import (
    ChatRequest
)

@Resource.app.post("/chat/completion/{user_id}")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest
):
    """
    Endpoint for chat
    """
    chat_coroutine = Resource.core.chat(
        user_id = user_id,
        message = request.message,
        history_messages = request.history_messages,
        history_msg_role_map = request.history_msg_role_map,
        user_info = request.user_info,
        role = request.role,
        assistant_role = request.assistant_role,
        role_name = request.role_name,
        extra_template_fields = request.extra_template_fields,
        temporary_prompt = request.temporary_prompt,
        additional_data = request.additional_data,
        model_uid = request.model_uid,
        thinking = request.thinking,
        print_chunk = True,
        load_prompt = request.load_prompt,
        save_context = request.save_context,
        save_new_only = request.save_new_only,
        cross_user_data_routing = request.cross_user_data_routing,
        stream = request.stream
    )
    try:
        response = await Resource.chat_task_pool.run_task(user_id, chat_coroutine)
    except asyncio.CancelledError:
        raise HTTPException(
            message = "Chat Completion Task Cancelled or System Abnormal Shutdown.",
            status_code = 409 # Conflict
        )
        
    if isinstance(response, Response):
        return ORJSONResponse(
            response.model_dump(
                exclude_defaults = True
            ),
            status_code=response.status
        )
    else:
        async def generator_wrapper(context: AsyncIterator[CompletionsAPI.Delta]) -> AsyncIterator[bytes]:
            async for chunk in context:
                yield orjson.dumps(chunk.model_dump(exclude_none=True)) + b"\n"

        return StreamingResponse(generator_wrapper(response), media_type="application/x-ndjson")
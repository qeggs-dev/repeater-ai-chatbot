from typing import AsyncIterator
import orjson
from environs import Env
env = Env()
env.read_env()
from fastapi.responses import (
    ORJSONResponse,
    StreamingResponse
)
from fastapi.exceptions import (
    HTTPException
)
from ..._resource import Resource
from ....Assist_Struct import Response
from ....CallAPI import CompletionsAPI

import orjson

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
    context = await Resource.core.chat(
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
    if isinstance(context, Response):
        return ORJSONResponse(
            context.model_dump(
                exclude_defaults = True
            ),
            status_code=200
        )
    else:
        async def generator_wrapper(context: AsyncIterator[CompletionsAPI.Delta]) -> AsyncIterator[bytes]:
            async for chunk in context:
                yield orjson.dumps(chunk.model_dump(exclude_none=True)) + b"\n"

        return StreamingResponse(generator_wrapper(context), media_type="application/x-ndjson")
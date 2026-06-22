import orjson
from typing import AsyncGenerator

from core.call_api.image.generate._objects._completed_image_event import CompletedImageEvent
from core.call_api.image.generate._objects._partial_image_event import PartialImageEvent

from .....call_api.image import (
    ImageGenerateCaller,
    ImagesRequest as ImagesRequest,
    ImagesRuntime,
    ImagesResponse
)
from .....global_config_manager import ConfigManager
from .....runtime_container import RuntimeContainer
from ._router import image_router
from ._request import Request
from fastapi.responses import (
    ORJSONResponse,
    StreamingResponse
)

@image_router.post("/generate/{user_id}")
async def generate_image(
    user_id: str,
    request: Request,
):
    """
    Generate image from prompt.
    """
    runtime = RuntimeContainer.get_runtime()
    model_client = runtime.model_info_client
    user_config_manager = runtime.user_config_manager
    user_configs = await user_config_manager.load(user_id)
    global_configs = ConfigManager.get_configs()

    model_id = request.model_id
    if model_id is None:
        model_id = user_configs.model_id
    if model_id is None:
        model_id = global_configs.model_api.default_model_id
    
    model = await model_client.get_random_model(
        model_id
    )

    openai_pool = runtime.openai_pool
    image_generate_caller = ImageGenerateCaller(
        max_concurrency = 1000
    )

    header = {
        "User-Agent": global_configs.system_identification.system_ua
    }

    image_request = ImagesRequest(
        url = model.get_base_url(),
        proxy = model.proxy,
        limits = model.limits,
        headers = header,
        timeout = model.timeout,
        prompt = request.prompt,
    )

    image_runtime = ImagesRuntime(
        client_pool = openai_pool
    )

    result: AsyncGenerator[PartialImageEvent | CompletedImageEvent, None] | ImagesResponse = await image_generate_caller.call(
        image_request,
        image_runtime
    )

    if isinstance(result, ImagesResponse):
        return ORJSONResponse(
            result.model_dump(),
            status_code = 200
        )
    else:
        async def stream(result: AsyncGenerator[PartialImageEvent | CompletedImageEvent, None]):
            async for image in result:
                yield orjson.dumps(image.model_dump())
        
        return StreamingResponse(
            stream(result),
            status_code = 200
        )
        
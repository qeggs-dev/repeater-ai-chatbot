from typing import (
    Any,
    AsyncGenerator
)
from openai import (
    AsyncStream, omit
)
from openai.types import (
    ImagesResponse as OpenAIImagesResponse,
    ImageGenPartialImageEvent,
    ImageGenCompletedEvent
)
from ....pools.awaitable_pool import CoroutinePool
from ._objects import (
    ImagesRequest,
    ImagesRuntime,
    ImagesResponse,
    Background,
    Image,
    OutputFormat,
    Quality,
    ImageSize,
    ImageTokenUsage,
    ImageUsageTokensDetails,
    PartialImageEvent,
    CompletedImageEvent,
)

class ImageGenerateCaller:
    def __init__(self, max_concurrency: int = 100):
        self.coroutine_pool = CoroutinePool(max_concurrency)
    
    def none_to_omit(self, value: Any):
        if value is None:
            return omit
        return value
    
    async def call(self, request: ImagesRequest, runtime: ImagesRuntime) -> ImagesResponse:
        return await self.coroutine_pool.submit(
            self._parse_response(request, runtime)
        )
    
    async def _call(self, request: ImagesRequest, runtime: ImagesRuntime) -> ImagesResponse | AsyncStream[ImageGenPartialImageEvent | ImageGenCompletedEvent]:
        client = runtime.client
        response: AsyncStream[ImageGenPartialImageEvent | ImageGenCompletedEvent] = await client.images.generate(
            prompt = request.prompt,
            background = self.none_to_omit(request.background),
            model = self.none_to_omit(request.model),
            moderation = self.none_to_omit(request.moderation),
            n = self.none_to_omit(request.n),
            output_compression = self.none_to_omit(request.output_compression),
            output_format = self.none_to_omit(request.output_format),
            partial_images = self.none_to_omit(request.partial_images),
            quality = self.none_to_omit(request.quality),
            response_format = self.none_to_omit(request.response_format),
            size = self.none_to_omit(request.size),
            stream = request.stream,
            style = self.none_to_omit(request.style),
            user = self.none_to_omit(request.user),
            timeout = request.timeout
        )

        if request.stream:
            parsed_response = self._parse_stream_response(response)
        else:
            parsed_response = await self._parse_response(response)

        return parsed_response

    async def _parse_stream_response(self, response: AsyncStream[ImageGenPartialImageEvent | ImageGenCompletedEvent]) -> AsyncGenerator[PartialImageEvent | CompletedImageEvent, None]:
        async for event in response:
            if isinstance(event, ImageGenPartialImageEvent):
                yield PartialImageEvent(
                    b64_json = event.b64_json,
                    background = event.background,
                    created_at = event.created_at,
                    output_format = event.output_format,
                    partial_image_index = event.partial_image_index,
                    quality = event.quality,
                    size = event.size,
                    type = event.type
                )
            elif isinstance(event, ImageGenCompletedEvent):
                yield CompletedImageEvent(
                    b64_json = event.b64_json,
                    background = event.background,
                    created_at = event.created_at,
                    output_format = event.output_format,
                    quality = event.quality,
                    size = event.size,
                    type = event.type
                )
            else:
                raise Exception(f"Unknown event type: {event}")
        

    async def _parse_response(self, response: OpenAIImagesResponse) -> ImagesResponse:
        image_response = ImagesResponse()
        if response.created:
            image_response.created = response.created
        if response.background:
            image_response.background = Background(response.background)
        if response.data:
            image_response.data = []
            for image in response.data:
                response_image = Image()
                if image.b64_json:
                    response_image.b64_json = image.b64_json
                if image.revised_prompt:
                    response_image.revised_prompt = image.revised_prompt
                if image.url:
                    response_image.url = image.url
                image_response.data.append(response_image)
        if response.output_format:
            image_response.output_format = OutputFormat(response.output_format)
        if response.quality:
            image_response.quality = Quality(response.quality)
        if response.size:
            try:
                image_response.size = ImageSize(response.size)
            except ValueError:
                image_response.size = response.size
        if response.usage:
            image_response.usage = ImageTokenUsage(
                input_tokens = response.usage.input_tokens,
                output_tokens = response.usage.output_tokens,
                total_tokens  = response.usage.total_tokens,
            )
            if response.usage.input_tokens_details:
                image_response.usage.input_tokens_details = ImageUsageTokensDetails(
                    image_tokens = response.usage.input_tokens_details.image_tokens,
                    text_tokens = response.usage.input_tokens_details.text_tokens,
                )
            if response.usage.output_tokens_details:
                image_response.usage.output_tokens_details = ImageUsageTokensDetails(
                    image_tokens = response.usage.output_tokens_details.image_tokens,
                    text_tokens = response.usage.output_tokens_details.text_tokens,
                )
        return image_response
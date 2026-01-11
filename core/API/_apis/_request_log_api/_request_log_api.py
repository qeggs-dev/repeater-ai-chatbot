from ..._resource import Resource
import orjson
from typing import AsyncIterator
from fastapi.responses import ORJSONResponse, StreamingResponse

@Resource.app.get("/request_log")
@Resource.app.get("/request_log/list")
async def get_request_log():
    """
    Endpoint for getting request log
    
    Args:
        filter: Optional list of filters
    
    Returns:
        ORJSONResponse: Filtered log object dictionary
    """
    logs = await Resource.core.request_log.read_request_log()
    return ORJSONResponse([log.model_dump() for log in logs])

@Resource.app.get("/request_log/stream")
async def stream_request_log():
    """
    Endpoint for getting request log
    
    Args:
        filter: Optional list of filters
    
    Returns:
        StreamingResponse: Filtered log object dictionary
    """
    async def generate_jsonl() -> AsyncIterator[bytes]:
        """生成JSONL格式的字节流"""
        async for log in Resource.core.request_log.read_stream_request_log():
            yield orjson.dumps(log.model_dump()) + b"\n"

    return StreamingResponse(
        generate_jsonl(),
        media_type="application/x-ndjson",
        headers={
            "X-Content-Type-Options": "nosniff",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
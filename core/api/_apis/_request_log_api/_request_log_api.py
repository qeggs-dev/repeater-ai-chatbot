from ....server import Server
from ._router import request_log_router
import orjson
from typing import AsyncIterator
from fastapi.responses import ORJSONResponse, StreamingResponse

@request_log_router.get("/")
@request_log_router.get("/list")
async def get_request_log():
    """
    Endpoint for getting request log
    
    Args:
        filter: Optional list of filters
    
    Returns:
        ORJSONResponse: Filtered log object dictionary
    """
    logs = await Server.core.runtime.request_log.read_request_log()
    return ORJSONResponse([log.model_dump() for log in logs])

@request_log_router.get("/stream")
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
        async for log in Server.core.runtime.request_log.read_stream_request_log():
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
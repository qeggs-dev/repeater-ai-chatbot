from .._resource import chat, app
import orjson
from typing import AsyncIterator, Any, Dict, Union
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

class Filter(BaseModel):
    """
    Filter model for calllog
    """
    key: str
    value: str | int | float | bool | None = None

class RangeFilter(BaseModel):
    """
    Range filter model for calllog
    """
    key: str
    min: int | float | None = None
    max: int | float | None = None

class FilterList(BaseModel):
    """
    Filter list model for calllog
    """
    filters: list[Filter | RangeFilter]

def apply_filters(log_obj_dict: dict, filter_map: dict) -> bool:
    """
    应用过滤器到日志对象
    
    Args:
        log_obj_dict: 日志对象字典
        filter_map: 过滤器映射字典
    
    Returns:
        bool: 是否通过过滤
    """
    if not filter_map:
        return True
        
    for key, filter_obj in filter_map.items():
        if key not in log_obj_dict:
            # 如果过滤器键不存在于日志中，跳过这个过滤器
            continue
            
        value = log_obj_dict[key]
        
        if isinstance(filter_obj, Filter):
            if value != filter_obj.value:
                return False
        elif isinstance(filter_obj, RangeFilter):
            value_min = filter_obj.min if filter_obj.min is not None else float('-inf')
            value_max = filter_obj.max if filter_obj.max is not None else float('inf')
            
            if value < value_min or value > value_max:
                return False
    return True

async def generate_calllog(filter: FilterList | None = None) -> AsyncIterator[Dict[str, Any]]:
    """
    生成通话日志的异步生成器
    
    Args:
        filter: 可选的过滤器列表
    
    Yields:
        过滤后的日志对象字典
    """
    # 获取日志生成器
    generator = chat.calllog.read_stream_call_log()

    # 将过滤器转换为字典
    if filter:
        filter_map: dict[str, Filter | RangeFilter] = {}
        for f in filter.filters:
            filter_map[f.key] = f
    else:
        filter_map = {}

    # 将每个日志对象转换为字典并应用过滤
    async for log_obj in generator:
        log_obj_dict = log_obj.as_dict
        if apply_filters(log_obj_dict, filter_map):
            yield log_obj_dict

@app.get("/calllog")
async def get_calllog(filter: FilterList | None = None):
    """
    Endpoint for getting calllog
    
    Args:
        filter: 可选的过滤器列表
    
    Returns:
        JSONResponse: 包含通话日志的JSON响应
    """
    logs = [calllog async for calllog in generate_calllog(filter=filter)]
    return JSONResponse(logs)

@app.get("/calllog/stream")
async def stream_call_logs(filter: FilterList | None = None):
    """
    流式传输通话日志
    
    Args:
        filter: 可选的过滤器列表
    
    Returns:
        StreamingResponse: JSONL格式的流式响应
    """
    async def generate_jsonl() -> AsyncIterator[bytes]:
        """生成JSONL格式的字节流"""
        async for log in generate_calllog(filter=filter):
            yield orjson.dumps(log) + b"\n"

    return StreamingResponse(
        generate_jsonl(),
        media_type="application/x-ndjson",
        headers={
            "X-Content-Type-Options": "nosniff",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
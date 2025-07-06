from .._resource import chat, app
import orjson
from fastapi.responses import JSONResponse, StreamingResponse

@app.get("/calllog")
async def get_calllog():
    """
    Endpoint for getting calllog
    """

    # 获取calllog
    calllogs = await chat.calllog.read_call_log()

    # 将calllog转换为字典列表
    calllog_list = [calllog_object.as_dict for calllog_object in calllogs]

    # 返回JSON响应
    return JSONResponse(calllog_list)

@app.get("/calllog/stream")
async def stream_call_logs():
    async def generate_jsonl():
        """
        将日志流转换为JSONL流格式
        """
        # 获取日志生成器
        generator = chat.calllog.read_stream_call_log()

        # 将每个日志对象转换为字典并使用orjson序列化
        async for log_obj in generator:
            # 转换为字典并使用orjson序列化
            json_line = orjson.dumps(
                log_obj.as_dict,
                option=orjson.OPT_APPEND_NEWLINE
            )

            # 生成JSONL行
            yield json_line

    return StreamingResponse(
        generate_jsonl(),
        media_type="application/x-ndjson",  # 保持JSONL格式
        headers={
            # 关键：不设置Content-Disposition，避免浏览器触发下载
            "X-Content-Type-Options": "nosniff",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
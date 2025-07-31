from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger
import traceback
import time

from .._resource import app

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # 记录异常日志
        try:
            traceback_info = traceback.format_exc()
            logger.error("API call failed: \n{traceback}", user_id = "[System]", traceback = traceback_info)
        except KeyError:
            logger.error("Exception: {exception}", exception = e)
        return JSONResponse(
            status_code=500,
            content={
                "message": "服务器内部错误",
                "error": str(e),
                "time": time.time_ns() // 10**6,
            },
        )
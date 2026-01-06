from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import AsyncIterator
from ..Lifespan import StartHandler, ExitHandler
from ._resource import Resource

# 定义生命周期管理器
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    if not Resource.inited():
        raise RuntimeError("Repeater API Resource not inited!")
    await StartHandler.execute()
    yield
    await ExitHandler.execute()
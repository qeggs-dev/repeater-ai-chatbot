import asyncio
from typing import (
    Any,
    Coroutine,
    TypeVar,
)
from loguru import logger
from pydantic import validate_call
import inspect

T = TypeVar("T")

class CoroutinePool:
    @validate_call
    def __init__(self, max_concurrency: int = 1000):
        # 协程池
        self._max_concurrency = max_concurrency
        self._semaphore = asyncio.Semaphore(self._max_concurrency)
        self._tasks = set()  # 存储运行中的任务
    
    # region 协程池管理
    async def submit(self, coro: Coroutine[None, None, T], user_id: str | None = None) -> T:
        """提交任务到协程池，并等待返回结果"""
        async with self._semaphore:  # 控制并发数
            task = asyncio.create_task(coro)
            self._tasks.add(task)
            currentframe = inspect.currentframe()
            if currentframe is None:
                raise RuntimeError("No current frame")
            else:
                back_frame = currentframe.f_back
                if back_frame is None:
                    parten = "<Main Module>"
                else:
                    parten = back_frame.f_code.co_name
            logger.debug(
                "Created a new task for {parten} ({task_number}/{max_concurrency})",
                parten = parten,
                task_number = len(self._tasks),
                max_concurrency = self._max_concurrency,
                user_id = user_id
            )
            try:
                result = await task
                return result
            finally:
                self._tasks.remove(task)
                logger.debug(
                    "Removed a task ({task_number}/{max_concurrency})",
                    task_number = len(self._tasks),
                    max_concurrency = self._max_concurrency,
                    user_id = user_id
                )
        
    async def shutdown(self):
        """关闭池，等待所有任务完成"""
        await asyncio.gather(*self._tasks)

    @validate_call
    async def set_concurrency(self, new_max: int):
        """动态修改并发限制"""
        self._max_concurrency = new_max
        self._semaphore = asyncio.Semaphore(new_max)
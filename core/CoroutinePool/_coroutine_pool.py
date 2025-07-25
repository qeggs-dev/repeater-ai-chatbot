import asyncio
from typing import (
    Any,
    Awaitable,
    TypeVar,
)
from loguru import logger
import inspect

T = TypeVar('T')

class CoroutinePool:
    def __init__(self, max_concurrency: int | None = None):
        # 协程池
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.tasks = set()  # 存储运行中的任务
    # region 协程池管理
    async def submit(self, coro: Awaitable[T], user_id: str = "[System]") -> T:
        """提交任务到协程池，并等待返回结果"""
        async with self.semaphore:  # 控制并发数
            task = asyncio.create_task(coro)
            self.tasks.add(task)
            logger.debug(f'Created a new task for {inspect.currentframe().f_back.f_code.co_name} ({len(self.tasks)}/{self.max_concurrency})', user_id = user_id)
            try:
                result = await task
                return result
            finally:
                self.tasks.remove(task)
                logger.debug(f'Removed a task ({len(self.tasks)}/{self.max_concurrency})', user_id = user_id)
        
    async def shutdown(self):
        """关闭池，等待所有任务完成"""
        await asyncio.gather(*self.tasks)

    async def set_concurrency(self, new_max: int):
        """动态修改并发限制"""
        self.max_concurrency = new_max
        self.semaphore = asyncio.Semaphore(new_max)
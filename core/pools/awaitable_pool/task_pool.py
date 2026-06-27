import asyncio

from typing import (
    Any,
    Coroutine,
    TypeVar,
)
from loguru import logger
from ..lock_pool import AsyncLockPool

T = TypeVar("T")

class TaskPool:
    def __init__(self, max_concurrency: int = 1000):
        self._max_concurrency = max_concurrency
        self._semaphore = asyncio.Semaphore(self._max_concurrency)
        self._tasks: dict[str, dict[str, asyncio.Task]] = {}
        self._pool_locks: AsyncLockPool = AsyncLockPool()
    
    async def run_task(
            self,
            user_id: str,
            task_id: str,
            coro: Coroutine[None, None, T]
        ) -> T:
        """提交任务到任务池，并等待返回结果"""
        async with self._semaphore:  # 控制并发数
            task: asyncio.Task[T] = asyncio.create_task(coro)
            async with await self._pool_locks.get_lock(user_id):
                if user_id not in self._tasks:
                    self._tasks[user_id] = {}
                self._tasks[user_id][task_id] = task
            
            try:
                return await task
            finally:
                async with await self._pool_locks.get_lock(user_id):
                    if user_id in self._tasks:
                        tasks = self._tasks[user_id]
                        tasks.pop(task_id, None)
                        if not tasks:
                            del self._tasks[user_id]
            
    
    async def cancel_tasks(self, user_id: str):
        """取消指定用户的所有任务"""
        async with await self._pool_locks.get_lock(user_id):
            cancel_count = 0
            if user_id in self._tasks:
                tasks = self._tasks[user_id]
                for task_id, task in tasks.items():
                    if task.cancel():
                        cancel_count += 1
                        tasks.pop(task_id, None)
                if not tasks:
                    del self._tasks[user_id]
            return cancel_count
    
    async def cancel_task(self, user_id: str, task_id: str):
        """取消指定任务"""
        async with await self._pool_locks.get_lock(user_id):
            if user_id in self._tasks:
                tasks = self._tasks[user_id]
                if task_id in tasks:
                    task = tasks[task_id]
                    if task.cancel():
                        del tasks[task_id]
                        if not tasks:
                            del self._tasks[user_id]
                        return True
                    else:
                        return False
            return False
        
    async def shutdown(self):
        """关闭池，等待所有任务完成"""
        await asyncio.gather((task for task in tasks) for tasks in self._tasks.values())

    async def set_concurrency(self, new_max: int):
        """动态修改并发限制"""
        self._max_concurrency = new_max
        self._semaphore = asyncio.Semaphore(new_max)
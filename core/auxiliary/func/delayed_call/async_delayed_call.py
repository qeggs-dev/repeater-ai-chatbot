import asyncio
from typing import (
    Callable,
    Awaitable,
    Any,
    AsyncGenerator,
    TypeVar,
    Generic
)

T = TypeVar("T")

class ADelayedCall(Generic[T]):
    def __init__(self, func: Callable[..., Awaitable[T]]):
        self.func = func
        self.queue = asyncio.Queue()
    
    async def __call__(self, *args, **kwargs):
        await self.queue.put((args, kwargs))
    
    async def run(self) -> AsyncGenerator[T, None]:
        while not self.queue.empty():
            args, kwargs = self.queue.get()
            result = await self.func(*args, **kwargs)
            yield result
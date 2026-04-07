from typing import Generic, TypeVar

from ..lock_pool import AsyncLockPool

T = TypeVar("T")

class ResourcePool(Generic[T]):
    def __init__(self):
        self._resources: dict[str, T] = {}
        self._lock_pool = AsyncLockPool()
    
    def __contains__(self, id: str) -> bool:
        return id in self._resources

    async def add_resource(self, id: str, resource: T):
        async with await self._lock_pool.get_lock(id):
            self._resources[id] = resource
    
    async def get_resource(self, id: str) -> T:
        async with await self._lock_pool.get_lock(id):
            return self._resources[id]
    
    async def remove_resource(self, id: str):
        async with await self._lock_pool.get_lock(id):
            del self._resources[id]
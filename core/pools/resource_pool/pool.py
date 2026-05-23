from typing import Generic, TypeVar, Generator

from ..lock_pool import AsyncLockPool

T_Id = TypeVar("T_Id")
T_Resource = TypeVar("T_Resource")

class ResourcePool(Generic[T_Id, T_Resource]):
    def __init__(self):
        self._resources: dict[T_Id, T_Resource] = {}
        self._lock_pool = AsyncLockPool()
    
    def __contains__(self, id: T_Id) -> bool:
        return id in self._resources
    
    def __bool__(self) -> bool:
        return bool(self._resources)

    async def add(self, id: T_Id, resource: T_Resource):
        async with await self._lock_pool.get_lock(id):
            self._resources[id] = resource
    
    async def get(self, id: T_Id) -> T_Resource:
        async with await self._lock_pool.get_lock(id):
            return self._resources[id]
    
    async def remove(self, id: T_Id):
        async with await self._lock_pool.get_lock(id):
            if id in self._resources:
                del self._resources[id]
    
    @property
    def ids(self) -> list[T_Id]:
        return list(self._resources.keys())
    
    @property
    def resources(self) -> list[T_Resource]:
        return list(self._resources.values())
    
    def items(self) -> Generator[tuple[T_Id, T_Resource], None, None]:
        return (resource for resource in self._resources.items())
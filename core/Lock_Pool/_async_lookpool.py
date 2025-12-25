from __future__ import annotations
import asyncio
from typing import TypeVar, Generic
from loguru import logger

T_KEY = TypeVar("T_KEY")

class LockPool(Generic[T_KEY]):
    def __init__(self):
        self._lock = asyncio.Lock()
        self.locks: dict[T_KEY, asyncio.Lock] = {}
        self._reference_count : dict[T_KEY, int] = {}
    
    
    async def get_lock(self, key: T_KEY) -> asyncio.Lock:
        async with self._lock:
            if key in self.locks:
                logger.debug(f"LockPool: Get lock for {repr(key)}")
                return self.locks[key]
            
            class Packaged_Lock(asyncio.Lock):
                def _increase_reference_counting(inner_self):
                    if key not in self._reference_count:
                        if key not in self.locks:
                            self.locks[key] = inner_self
                        self._reference_count[key] = 1
                    else:
                        self._reference_count[key] += 1
                
                def _reduce_reference_counting(inner_self):
                    if self._reference_count[key] > 0:
                        self._reference_count[key] -= 1
                    else:
                        if key in self.locks:
                            del self.locks[key]
                        del self._reference_count[key]
                
                @property
                def reference_count(inner_self):
                    return self._reference_count.get(key, 0)
                
                async def acquire(inner_self):
                    inner_self._increase_reference_counting()
                    logger.debug(f"LockPool: Acquiring lock for {repr(key)}({inner_self.reference_count})")
                    try:
                        await super().acquire()
                    except Exception as e:
                        inner_self._reduce_reference_counting()
                        logger.warning(f"LockPool: Failed to acquire lock for {repr(key)}: {e}")
                        raise

                def release(inner_self):
                    try:
                        super().release()
                        inner_self._reduce_reference_counting()
                        logger.debug(f"LockPool: Released lock for {repr(key)}({inner_self.reference_count})")
                    except Exception as e:
                        logger.warning(f"LockPool: Failed to release lock for {repr(key)}: {e}")
                        raise
            
            lock = Packaged_Lock()
            logger.debug(f"LockPool: Created lock for {repr(key)}")
            self.locks[key] = lock
            return lock
        
    async def lock_count(self, key: T_KEY):
        async with self._lock:
            return self._reference_count.get(key, 0)
        
    def __contains__(self, key: T_KEY) -> bool:
        return key in self.locks
    
    def __len__(self) -> int:
        return len(self.locks)
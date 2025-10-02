from __future__ import annotations
import threading
from typing import TypeVar
from loguru import logger

T_KEY = TypeVar('T_KEY')

class LockPool:
    def __init__(self):
        self._lock = threading.Lock()
        self.locks: dict[T_KEY, threading.Lock] = {}
        self._reference_count : dict[T_KEY, int] = {}
    
    def get_lock(self, key: T_KEY) -> threading.Lock:
        with self._lock:
            if key in self.locks:
                logger.debug(f"LockPool: Get lock for {key}")
                return self.locks[key]
            class Packaged_Lock(threading.Lock):
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
                
                def acquire(inner_self):
                    inner_self._increase_reference_counting()
                    logger.debug(f'LockPool: Acquiring lock for {key}')
                    try:
                        super().acquire()
                    except Exception as e:
                        logger.warning(f'LockPool: Failed to acquire lock for {key}: {e}')
                        inner_self._reduce_reference_counting()
                        raise
                def release(inner_self):
                    try:
                        super().release()
                        logger.debug(f'LockPool: Releasing lock for {key}')
                        inner_self._reduce_reference_counting()
                    except Exception as e:
                        logger.warning(f'LockPool: Failed to release lock for {key}: {e}')
                        raise
            
            lock = Packaged_Lock()
            self.locks[key] = lock
            logger.debug(f"LockPool: Created lock for {key}")
            return lock
    def lock_count(self, key: T_KEY):
        with self._lock:
            return self._reference_count.get(key, 0)
    def __contains__(self, key: T_KEY) -> bool:
        return key in self.locks
    def __len__(self) -> int:
        return len(self.locks)
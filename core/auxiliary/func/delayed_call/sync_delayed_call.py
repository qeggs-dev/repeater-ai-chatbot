from queue import Queue
from typing import (
    Callable,
    Any,
    Generator,
    TypeVar,
    Generic,
)

T = TypeVar("T")

class SDelayedCall(Generic[T]):
    def __init__(self, func: Callable[..., T]):
        self.func = func
        self.queue = Queue()
    
    def __call__(self, *args, **kwargs):
        self.queue.put((args, kwargs))
    
    def run(self) -> Generator[T, None, None]:
        while not self.queue.empty():
            args, kwargs = self.queue.get()
            result = self.func(*args, **kwargs)
            yield result
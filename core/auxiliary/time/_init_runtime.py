import time
import traceback
from types import TracebackType

from typing import Any, Callable, Type
from loguru import logger

class PrintInitRuntime:
    def __init__(self, task_name: str):
        self.task_name = task_name
        self._start_time: int = 0
        self._end_time: int = 0
    
    def __enter__(self) -> None:
        logger.info(
            "Initializing {name}...",
            name = self.task_name
        )
        self._start_time = time.perf_counter_ns()

    def __exit__(self, exc_type: Type[Exception] | None, exc_val: Exception | None, exc_tb: TracebackType | None) -> None:
        self._end_time = time.perf_counter_ns()
        if exc_type is None:
            logger.info(
                "Initialized {name} in {time} ms.",
                name = self.task_name,
                time = (self._end_time - self._start_time) / 1e6
            )
        else:
            logger.error(
                "Failed to initialize {name} in {time} ms.\n{exc_msg}",
                name = self.task_name,
                time = (self._end_time - self._start_time) / 1e6,
                exc_msg = str(exc_val),
                exc_tb = traceback.format_tb(exc_tb)
            )

def print_init_runtime(task_name: str):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with PrintInitRuntime(task_name):
                result = func(*args, **kwargs)
            return result
        wrapper.raw_func = func
        return wrapper
    return decorator
from contextlib import contextmanager
from typing import Generator, Generic, TypeVar
from loguru import logger

T_Key = TypeVar("T_Key")
T_Value = TypeVar("T_Value")

class StatusMap(Generic[T_Key, T_Value]):
    def __init__(self):
        self.status_map: dict[T_Key, list[T_Value]] = {}
    
    def enter_status(self, key: T_Key, status: T_Value) -> None:
        if key not in self.status_map:
            self.status_map[key] = []
        self.status_map[key].append(status)
        logger.trace(
            "enter status: {key} <- {status}",
            key = key,
            status = status
        )
    
    def exit_last_status(self, key: T_Key) -> None:
        if key in self.status_map:
            stack = self.status_map[key]
            last_status = stack.pop()
            logger.trace(
                "exit status: {key} -> {last_status}",
                key = key,
                last_status = last_status
            )
            if not stack and key in self.status_map:
                del self.status_map[key]

    def get_status(self, key: T_Key) -> list[T_Value]:
        return self.status_map[key]
    
    def contains(self, key: T_Key) -> bool:
        return key in self.status_map
    
    def __contains__(self, key: T_Key) -> bool:
        return self.contains(key)

    @contextmanager
    def enter(self, key: T_Key, status: T_Value) -> Generator[None, None, None]:
        self.enter_status(key, status)
        try:
            yield
        finally:
            self.exit_last_status(key)

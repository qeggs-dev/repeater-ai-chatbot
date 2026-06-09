from contextlib import contextmanager
from typing import Generator, Generic, TypeVar
from loguru import logger

T_Value = TypeVar("T_Value")

class StatusStack(Generic[T_Value]):
    def __init__(self):
        self.status_stack: list[T_Value] = []
    
    def enter_status(self, status: T_Value) -> None:
        self.status_stack.append(status)
        logger.trace(
            "enter status: stack <- {status}",
            status = status
        )
    
    def exit_last_status(self) -> T_Value | None:
        last_status = self.status_stack.pop()
        logger.trace(
            "exit status: stack -> {last_status}",
            last_status = last_status
        )
        return last_status

    def get_status(self) -> list[T_Value]:
        return self.status_stack

    @contextmanager
    def enter(self, status: T_Value) -> Generator[None, None, None]:
        self.enter_status(status)
        try:
            yield
        finally:
            self.exit_last_status()

from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")

@dataclass
class Args(Generic[T]):
    """
    Args class
    """
    args: tuple[T, ...]
    kwargs: dict[str, T]
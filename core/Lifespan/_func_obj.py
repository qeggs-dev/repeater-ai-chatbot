from dataclasses import dataclass
from ._args import Args
from typing import Callable, TypeVar, Generic

T = TypeVar('T', bound=Callable)

@dataclass
class FuncObject(Generic[T]):
    """A dataclass that represents a function object."""
    args: Args
    func: T

    def __call__(self, *args, **kwargs):
        """Calls the function with the given arguments."""
        return self.func(*args, **kwargs)
    

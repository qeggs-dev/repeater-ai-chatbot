from typing import TypeGuard, Iterable, TypeVar, Any

T = TypeVar("T")


def is_iterable(value: Iterable[T] | Any) -> TypeGuard[Iterable[T]]:
    if hasattr(value, "__iter__"):
        return True
    return False
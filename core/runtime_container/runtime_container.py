from __future__ import annotations

import ssl
from typing import ClassVar
from .runtime import RepeaterRuntime

class RuntimeContainer:
    _instance: ClassVar[RuntimeContainer] | None = None
    _objects: ClassVar[RepeaterRuntime] | None = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    @classmethod
    def init_runtime(cls) -> None:
        cls._objects = RepeaterRuntime()
    
    @classmethod
    def get_runtime(cls, init: bool = False) -> RepeaterRuntime:
        if cls._objects is None:
            if init:
                cls.init_runtime()
            else:
                raise RuntimeError("GlobalObjects not initialized")
        return cls._objects
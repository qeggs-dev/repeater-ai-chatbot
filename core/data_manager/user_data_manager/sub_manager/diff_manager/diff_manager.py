import os
import uuid
import orjson
import aiofiles
import jsonpatch

from pathlib import Path
from typing import Any
from .stream import BlockStream
from .index_loader import IndexLoader

class DiffManager:
    def __init__(self, base_path: str | os.PathLike):
        self._base_path = Path(base_path)
    
    async def submit(self, data: Any):
        async with IndexLoader(self._base_path) as index_loader:
            stream = BlockStream(self._base_path, index_loader)
            stream.submit(data)
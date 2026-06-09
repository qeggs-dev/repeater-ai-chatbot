import os
import uuid
import orjson
import aiofiles

from pathlib import Path
from .models import Index

class IndexLoader:
    def __init__(self, base_path: str | os.PathLike):
        self._base_path = Path(base_path)
        self._index: Index | None = None
    
    @property
    def _index_file(self) -> Path:
        return self._base_path / "index.json"
    
    @property
    def _diff_dir(self) -> Path:
        return self._base_path / "diffs"
    
    @property
    def _index_exists(self) -> bool:
        return self._index_file.exists()
    
    async def get_index(self) -> Index:
        if self._index is None:
            if not self._index_exists:
                index = Index(
                    start_file = str(uuid.uuid4()),
                )
                index.end_file = index.start_file
                await self.save_index(index)
                return index
        
            async with aiofiles.open(self._index_file, "rb") as f:
                return Index(**orjson.loads(await f.read()))
        else:
            return self.get_cache()
    
    async def save_index(self, index: Index) -> None:
        self.set_cache(index)
    
    def set_cache(self, index: Index) -> None:
        if not isinstance(index, Index):
            raise TypeError("index must be Index")
        self._index = index
    
    def get_cache(self) -> Index | None:
        return self._index
    
    async def submit_index(self, index: Index) -> None:
        async with aiofiles.open(self._index_file, "wb") as f:
            await f.write(orjson.dumps(index.model_dump()))
    
    async def __aenter__(self):
        await self.get_index()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.submit_index(self._index)
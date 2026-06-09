from pathlib import Path
from typing import (
    Iterator
)
from ..blocks import (
    ALL_BLOCKS,
    DATA_BLOCKS,
    HeadJumpModel,
    EndJumpModel,
)
from .get_blocks import get_blocks

class BlockReversedIterator:
    def __init__(self, base_path: Path, target_file: Path):
        self._base_path = base_path
        self._target_file = target_file
        self._get_blocks: Iterator[ALL_BLOCKS] = reversed([])
    
    @property
    def target_file(self) -> Path:
        return self._base_path / self._target_file

    async def set_target_file(self, target_file: Path):
        self._target_file = target_file
        self._get_blocks = reversed([block async for block in get_blocks(self._get_blocks)])

    async def __aenter__(self):
        if not self.target_file.exists():
            raise FileNotFoundError(f"{self.target_file} not found")
        await self.set_target_file(self._target_file)
        return self

    async def __anext__(self) -> DATA_BLOCKS:
        while True:
            block = self._get_blocks.__next__()
            
            if isinstance(block, HeadJumpModel):
                if block.target_file is not None:
                    await self.set_target_file(block.target_file)
                    continue
                else:
                    raise StopAsyncIteration
            if isinstance(block, EndJumpModel):
                continue
            break
        return block
from pathlib import Path
from ..blocks import (
    DATA_BLOCKS,
    HeadJumpModel,
    EndJumpModel,
)
from .get_blocks import get_blocks

class BlockIterator:
    def __init__(self, base_path: Path, target_file: Path):
        self._base_path = base_path
        self.set_target_file(target_file)
    
    @property
    def target_file(self) -> Path:
        return self._base_path / self._target_file

    def set_target_file(self, target_file: Path):
        self._target_file = target_file
        self._get_blocks = get_blocks(self._get_blocks)

    async def __aenter__(self):
        if not self.target_file.exists():
            raise FileNotFoundError(f"{self.target_file} not found")
        return self

    async def __anext__(self) -> DATA_BLOCKS:
        while True:
            block = await self._get_blocks.__anext__()
                
            if isinstance(block, HeadJumpModel):
                continue
            if isinstance(block, EndJumpModel):
                self.set_target_file(block.target_file)
                continue
            break
        return block
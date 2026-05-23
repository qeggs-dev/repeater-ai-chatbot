import os
import uuid
import orjson
import asyncio
import aiofiles
import jsonpatch

from pathlib import Path
from typing import (
    Any,
    AsyncGenerator,
    Iterable,
    Callable,
)
from .iterator import BlockIterator
from .reversed_iterator import BlockReversedIterator
from ..blocks import (
    ALL_BLOCKS,
    DATA_BLOCKS,
    HeadJumpModel,
    EndJumpModel,
    SnapShotModel,
    DiffModel
)
from ..index_loader import IndexLoader

class BlockStream:
    def __init__(
            self,
            base_path: str | os.PathLike,
            index_loader: IndexLoader | None = None,
            max_block: int = 1000,
            new_file_name: Callable[[str], str] = lambda x: str(uuid.uuid4()),
        ):
        self._base_path = Path(base_path)
        self._index_loader = index_loader or IndexLoader(base_path)
        self._max_block = max_block
        self._now_block_count: int | None = None
        self._new_file_name = new_file_name
    
    @property
    def _target_file(self) -> Path:
        index = self._index_loader.get_cache()
        if index is None:
            raise RuntimeError("Index is not loaded.")
        return self._base_path / index.start_file
    
    @property
    def _end_file(self) -> Path:
        index = self._index_loader.get_cache()
        if index is None:
            raise RuntimeError("Index is not loaded.")
        return self._base_path / index.end_file
    
    async def __aiter__(self) -> AsyncGenerator[DATA_BLOCKS, None]:
        return BlockIterator(self._base_path, self._target_file)
    
    def __reversed__(self) -> AsyncGenerator[DATA_BLOCKS, None]:
        return BlockReversedIterator(self._base_path, self._target_file)
    
    async def _update_block_count(self) -> None:
        async with aiofiles.open(self._target_file, "rb") as f:
            self._now_block_count = 0
            async for line in f:
                self._now_block_count += 1
    
    async def change_end_file(self, end_file: str) -> None:
        self._add_block([
            EndJumpModel(
                target_file = end_file,
            )
        ])
        index = await self._index_loader.get_index()
        raw_end_file = index.end_file
        index.end_file = end_file
        await self._index_loader.save_index(index)
        self._add_block([
            HeadJumpModel(
                target_file = raw_end_file
            )
        ])
    
    async def _add_block(self, blocks: Iterable[ALL_BLOCKS]) -> None:
        async with aiofiles.open(self._end_file, "ab") as f:
            for block in blocks:
                await f.write(
                    orjson.dumps(
                        block.model_dump(),
                    )
                )
    
    async def add_block(self, block: DiffModel) -> None:
        if self._now_block_count is None:
            await self._update_block_count()
        
        if self._now_block_count >= self._max_block:
            await self.change_end_file(self._new_file_name(self._target_file))
            self._now_block_count = 0
        
        write_stack: list[DATA_BLOCKS] = []
        
        latest_snapshot = await self.find_latest_snapshot()
        if latest_snapshot is not None:
            count, snapshot = latest_snapshot
            if count >= 10:
                new_snapshot = await self.gen_snapshot()
                await write_stack.append(new_snapshot)
        
        await write_stack.append(block)

        await self._add_block(write_stack)
    
    async def find_latest_snapshot(self) -> tuple[int, SnapShotModel] | None:
        count: int = 0
        async for block in reversed(self):
            count += 1
            if isinstance(block, SnapShotModel):
                return count, block
        return None
    
    async def gen_snapshot(self):
        diff_stack = []
        async for block in reversed(self):
            if isinstance(block, DiffModel):
                diff_stack.append(block)
            elif isinstance(block, SnapShotModel):
                snap_shot = block.data
                for diff in reversed(diff_stack):
                    snap_shot = jsonpatch.apply_patch(snap_shot, diff)
                return SnapShotModel(
                    data = snap_shot,
                )
            else:
                raise ValueError("Invalid block type")
        
        if len(diff_stack) > 0:
            diff_iter = reversed(diff_stack)
            snap_shot = next(diff_iter).data
            for diff in diff_iter:
                snap_shot = jsonpatch.apply_patch(snap_shot, diff)
            return SnapShotModel(
                data = snap_shot,
            )
        else:
            raise ValueError("No snapshot found")

    async def make_diff(self, data: Any) -> DiffModel:
        snapshot = await self.gen_snapshot()

        patch = jsonpatch.make_patch(snapshot.data, data)
        patch_doc = patch.patch

        rev_patch = jsonpatch.make_patch(data, snapshot.data)
        rev_patch_doc = rev_patch.patch

        block = DiffModel(
            diff = patch_doc,
            rdiff = rev_patch_doc,
        )

        return block
    
    async def submit(self, data: Any):
        block = await self.make_diff(data)
        await self.add_block(block)
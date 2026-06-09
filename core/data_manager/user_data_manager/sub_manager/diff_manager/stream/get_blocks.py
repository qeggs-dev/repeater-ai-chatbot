import orjson
import aiofiles

from typing import (
    AsyncGenerator,
)
from ..blocks import (
    Validator,
    ALL_BLOCKS,
)

async def get_blocks(target_file) -> AsyncGenerator[ALL_BLOCKS, None]:
    async with aiofiles.open(target_file, "rb") as f:
        async for line in f:
            data = orjson.loads(line)
            validator = Validator(block=data)
            yield validator.block
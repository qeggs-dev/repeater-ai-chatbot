import asyncio
from loguru import logger
from pathlib import Path

async def delete_image(user_id:str, render_output_image_dir: Path, filename: str):
    """
    删除图片
    """
    await asyncio.to_thread((render_output_image_dir / filename).unlink)
    logger.info(f"Deleted image {filename}", user_id = user_id)
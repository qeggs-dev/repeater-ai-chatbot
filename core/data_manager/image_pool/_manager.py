import aiofiles
import asyncio
from pathlib import Path
import uuid
from typing import Generator, Any
from ._image_obj import ImageObj

class ImagePoolManager:
    def __init__(self, base_path: str | Path):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, ImageObj] = {}
    
    async def new(self, data: bytes | bytearray, suffix: str = "") -> str:
        """保存新图片并返回文件ID"""
        file_id = self._generate_unique_id(suffix)
        file_path = self.base_path / f"{file_id}{suffix}"
        
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(data)
        
        # 创建并缓存ImageObj
        image_obj = ImageObj(file_path)
        self._cache[file_id] = image_obj
        
        return file_id
    
    def _generate_unique_id(self, suffix: str = "") -> str:
        """生成唯一文件ID"""
        max_attempts = 100
        for _ in range(max_attempts):
            file_id = str(uuid.uuid4())
            if not any(self.base_path.glob(f"{file_id}*")):
                return file_id
        raise RuntimeError("Failed to generate unique file ID")
    
    async def get(self, file_id: str) -> ImageObj:
        """获取图片对象"""
        # 检查缓存
        if file_id in self._cache:
            cached_obj = self._cache[file_id]
            if cached_obj.exists:  # 验证文件仍然存在
                return cached_obj
            else:
                del self._cache[file_id]
        
        # 查找文件
        files = list(self.base_path.glob(f"{file_id}*"))
        if not files:
            raise FileNotFoundError(f"File {file_id} not found")
        
        if len(files) > 1:
            raise ValueError(f"Multiple files found for ID {file_id}")
        
        image_obj = ImageObj(files[0])
        self._cache[file_id] = image_obj
        return image_obj
    
    async def delete(self, file_id: str) -> bool:
        """删除图片"""
        try:
            image_obj = await self.get(file_id)
            image_obj.path.unlink()  # 删除文件
            self._cache.pop(file_id, None)  # 清除缓存
            return True
        except (FileNotFoundError, Exception):
            return False
    
    def list_images(self) -> list[str]:
        """列出所有图片ID"""
        return [file.stem for file in self.base_path.iterdir() if file.is_file()]
    
    def list_images_stream(self) -> Generator[str, None, None]:
        """列出所有图片ID"""
        for file in self.base_path.iterdir():
            if file.is_file():
                yield file.stem
    
    def get_stats(self) -> dict:
        """获取存储统计信息"""
        files = list(self.base_path.glob("*"))
        total_size = sum(f.stat().st_size for f in files if f.is_file())
        
        return {
            "total_images": len(files),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }
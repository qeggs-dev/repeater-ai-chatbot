from dataclasses import dataclass
from pathlib import Path
import mimetypes
import base64
import aiofiles
import asyncio

@dataclass
class ImageObj:
    path: Path
    encoding: str = "utf-8"

    def __post_init__(self):
        if not self.exists:
            raise FileNotFoundError(f"Image file {self.path} does not exist")

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def extension(self) -> str:
        return self.path.suffix
    
    @property
    def stem(self) -> str:
        return self.path.stem
    
    @property
    def exists(self) -> bool:
        return self.path.exists()
    
    @property
    def size(self) -> int:
        return self.path.stat().st_size

    @property
    def mime_type(self) -> str:
        mime_type, _ = mimetypes.guess_type(self.path)

        if not mime_type or not mime_type.strip():
            return "application/octet-stream"
        return mime_type
    
    @property
    def full_base64(self) -> str:
        try:
            with open(self.path, "rb") as f:
                return base64.b64encode(f.read()).decode(self.encoding)
        except Exception:
            return ""
    
    @property
    def data_base64(self) -> str:
        return f"data:{self.mime_type};base64,{self.full_base64}"
    
    async def async_base64(self) -> str:
        try:
            async with aiofiles.open(self.path, "rb") as f:
                return base64.b64encode(await f.read()).decode(self.encoding)
        except Exception:
            return ""
    
    async def full_async_base64(self) -> str:
        return f"data:{self.mime_type};base64,{await self.async_base64()}"
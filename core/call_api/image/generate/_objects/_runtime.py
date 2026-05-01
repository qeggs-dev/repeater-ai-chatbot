from dataclasses import dataclass, field
from openai import AsyncOpenAI

@dataclass
class ImagesRuntime:
    client: AsyncOpenAI = field(default_factory=AsyncOpenAI)
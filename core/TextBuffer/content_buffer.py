from dataclasses import dataclass, field
from .text_buffer import TextBuffer

@dataclass
class ContentBuffer:
    reasoning_buffer: TextBuffer = field(default_factory=TextBuffer)
    content_buffer: TextBuffer = field(default_factory=TextBuffer)
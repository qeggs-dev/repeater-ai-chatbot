from dataclasses import dataclass, field
from .text_buffer import TextBuffer

@dataclass
class ContentBuffer:
    reasoning_buffer: TextBuffer = field(default_factory=TextBuffer)
    content_buffer: TextBuffer = field(default_factory=TextBuffer)
    tool_calls_arguments_buffer: dict[int, TextBuffer] = field(default_factory=dict)

    def __len__(self):
        return len(self.reasoning_buffer) + len(self.content_buffer) + len(self.tool_calls_arguments_buffer)
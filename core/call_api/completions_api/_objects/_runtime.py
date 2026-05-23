from dataclasses import dataclass, field
from ....pools.openai_pool import OpenAIPool
from ....status_map import StatusStack
from ....text_buffer import ContentBuffer
from ._response import Response

@dataclass
class Runtime:
    """
    The runtime of this request.
    """
    response: Response = field(default_factory = Response)
    client_pool: OpenAIPool = field(default_factory = OpenAIPool)
    status_stack: StatusStack[str] = field(default_factory = StatusStack)
    content_buffer: ContentBuffer = field(default_factory = ContentBuffer)
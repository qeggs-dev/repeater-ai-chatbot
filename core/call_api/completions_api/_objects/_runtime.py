from dataclasses import dataclass, field
from ....pools.client_pool import OpenaiPool
from ....status_map import StatusMap
from ....text_buffer import ContentBuffer
from ._response import Response

@dataclass
class Runtime:
    """
    The runtime of this request.
    """
    response: Response = field(default_factory = Response)
    client_pool: OpenaiPool = field(default_factory = OpenaiPool)
    status_map: StatusMap[str, str] = field(default_factory = StatusMap)
    content_buffer: ContentBuffer = field(default_factory = ContentBuffer)
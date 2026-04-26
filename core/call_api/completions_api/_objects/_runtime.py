from dataclasses import dataclass, field
from ....pools.client_pool import OpenaiPool
from ....status_map import StatusMap
from ....text_buffer import ContentBuffer

@dataclass
class Runtime:
    """
    The runtime of this request.
    """

    client_pool: OpenaiPool = field(default_factory = OpenaiPool)
    status_map: StatusMap[str, str] = field(default_factory = StatusMap)
    content_buffer: ContentBuffer = field(default_factory = ContentBuffer)
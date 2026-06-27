from enum import Enum, auto

class CallMode(Enum):
    """
    Tool calling mode
    """
    SYNC = auto()
    ASYNC = auto()
    SYNC_IN_THREAD = auto()
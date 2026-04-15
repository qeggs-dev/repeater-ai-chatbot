from enum import Enum, auto

class CallType(Enum):
    """
    Enum for the type of function call
    """
    SYNC = auto()
    ASYNC = auto()
    SYNC_IN_THREAD = auto()
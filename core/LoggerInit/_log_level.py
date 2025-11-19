from loguru import logger
from enum import IntEnum

class LogLevel(IntEnum):
    """Logger log levels."""
    TRACE = 5
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
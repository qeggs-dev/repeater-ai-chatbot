from enum import StrEnum

class FinishReason(StrEnum):
    STOP = "stop"
    LENGTH = "length"
    CONTENT_FILTER = "content_filter"
    TOOL_CALLS = "tool_calls"
    INSUFFICIENT_SYSTEM_RESOURCE = "insufficient_system_resource"
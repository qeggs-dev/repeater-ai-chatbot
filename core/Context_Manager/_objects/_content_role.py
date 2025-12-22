from enum import StrEnum

class ContentRole(StrEnum):
    """
    上下文角色
    """
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "tool"
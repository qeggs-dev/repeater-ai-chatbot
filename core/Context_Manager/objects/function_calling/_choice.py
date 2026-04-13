from enum import StrEnum

class Choice(StrEnum):
    """
    Enum for choices
    """
    NONE = "none"
    AUTO = "auto"
    REQUIRED = "required"
    FORCE = "force"
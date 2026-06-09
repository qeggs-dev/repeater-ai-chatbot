from enum import StrEnum

class ServiceTier(StrEnum):
    AUTO = "auto"
    DEFAULT = "default"
    STANDARD = "standard"
    FLEX = "flex"
    PRIORITY = "priority"
    RESERVED = "reserved"
class NexusException(Exception):
    """Base class for exceptions in this module."""
    pass


class InvalidUUIDError(NexusException):
    """Raised when a file UUID is invalid."""
    pass
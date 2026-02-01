class NexusException(Exception):
    """Base class for exceptions in this module."""
    pass


class InvalidUUIDError(NexusException):
    """Raised when a file UUID is invalid."""
    pass

class ResponseTypeError(NexusException):
    """Raised when a response type is invalid."""
    pass
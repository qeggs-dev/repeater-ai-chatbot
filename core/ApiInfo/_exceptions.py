class APIInfoException(Exception):
    """Base class for exceptions in this module."""
    pass


class APIGroupNotFoundError(APIInfoException):
    """Raised when an API group is not found."""
    pass

class APIKeyNotSetError(APIInfoException):
    """Raised when an API key is not set."""
    pass
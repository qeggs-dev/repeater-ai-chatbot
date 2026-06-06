import openai as _openai

class CallAPIException(Exception):
    """Base class for exceptions in this module."""
    pass

class APIError(CallAPIException, _openai.APIError):
    """Exception raised when the request is bad."""
    pass

class APIConnectionError(APIError, _openai.APIConnectionError):
    """Exception raised when the connection to the API fails."""
    pass

class APITimeoutError(APIConnectionError, _openai.APIConnectionError):
    """Exception raised when the request times out."""
    pass

class APIStatusError(APIError, _openai.APIStatusError):
    """Exception raised when the API returns a status code indicating an error."""
    pass

class ClientBadRequest(APIStatusError):
    """Exception raised when the request is bad."""
    pass

class BadRequestError(ClientBadRequest, _openai.BadRequestError):
    """Exception raised when the request is bad."""
    pass

class AuthenticationError(ClientBadRequest, _openai.AuthenticationError):
    """Exception raised when the request is not authenticated."""
    pass

class PermissionDeniedError(ClientBadRequest, _openai.PermissionDeniedError):
    """Exception raised when the request is not authorized."""
    pass

class NotFoundError(ClientBadRequest, _openai.NotFoundError):
    """Exception raised when the requested resource is not found."""
    pass

class ConflictError(ClientBadRequest, _openai.ConflictError):
    """Exception raised when the request conflicts with the current state of the resource."""
    pass

class UnprocessableEntityError(ClientBadRequest, _openai.UnprocessableEntityError):
    """Exception raised when the request is unprocessable."""
    pass

class RateLimitError(ClientBadRequest, _openai.RateLimitError):
    """Exception raised when the request exceeds the rate limit."""
    pass

class InternalServerError(APIStatusError):
    """Exception raised when the API returns a 500 status code."""
    pass

class UnknowAPIStatusError(APIStatusError):
    """Exception raised when the API returns an unknown status code."""
    pass

class StreamNotAvailable(CallAPIException):
    """Exception raised when the API does not support streaming."""
    pass
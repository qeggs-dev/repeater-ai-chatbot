from ..CallAPI.CompletionsAPI import Request

class ModelRequesterException(Exception):
    """Base class for exceptions in this module."""
    pass

class Regenerate(ModelRequesterException):
    """Let the model continue to generate content."""
    def __init__(self, request: Request):
        self.request = request
        super().__init__("The model has finished generating content.")
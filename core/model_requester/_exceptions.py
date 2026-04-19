from ..call_api.completions_api import Request

class ModelRequesterException(Exception):
    """Base class for exceptions in this module."""
    pass

class GenerateControl(ModelRequesterException):
    """Used to control the build process."""
    pass

class Regenerate(GenerateControl):
    """Let the model continue to generate content."""
    def __init__(self, request: Request):
        self.request = request
        super().__init__("The model has finished generating content.")

class GenerateFinished(GenerateControl):
    """Let the model stop generating content."""
    pass
class ConfigError(Exception):
    """Base class for exceptions in this module."""
    pass

class ConfigValidationError(ConfigError):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
        errors -- pydantic errors
    """
    def __init__(self, message: str, errors:list):
        self.message = message
        self.errors = errors
    
    def __str__(self):
        text = f"{self.message}\n"
        for error in self.errors:
            loc = ".".join([str(x) for x in error['loc']])
            text += f"\n---\n{loc}:"
            text += f"  - {error['msg']}\n"
            text += f"  - {error['type']}\n"
        return text

class ConfigSyntaxError(ConfigValidationError):
    """Exception raised for errors in the input."""
    pass
    

class ConfigFileLoadError(ConfigError):
    """Exception raised for errors in the loading file."""
    pass

class ConfigPackingError(ConfigValidationError):
    """Exception raised for errors in the packing config."""
    pass
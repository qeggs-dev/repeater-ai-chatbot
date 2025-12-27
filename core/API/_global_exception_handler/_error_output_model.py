from pydantic import BaseModel, ConfigDict


class ErrorResponse(BaseModel):
    """
    Error Output Model
    """
    model_config = ConfigDict(
        validate_assignment=True
    )

    error_message: str = "Internal Server Error"
    error_code: int = 500
    source_exception: str = ""
    exception_message: str = ""
    exception_traceback: str | None = None
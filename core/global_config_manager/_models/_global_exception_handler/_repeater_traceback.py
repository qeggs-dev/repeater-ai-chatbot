from pydantic import BaseModel, ConfigDict

class RepeaterTracebackConfig(BaseModel):
    enable: bool = True
    timeformat: str = "%Y-%m-%d %H:%M:%S"
    exclude_library_code: bool = True
    format_validation_error: bool = True
    record_warnings: bool = True
    traditional_stack_frame: bool = True
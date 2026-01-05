from pydantic import BaseModel, ConfigDict

class Global_Exception_Handler_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    error_message: str = "Internal Server Error"
    critical_error_message: str = "Critical Server Error!"
    crash_exit: bool = True
    traceback_save_to: str | None = None
    error_output_include_traceback: bool = False
    format_validation_error: bool = True
    record_warnings: bool = True
    record_all_exceptions: bool = False
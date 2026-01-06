from pydantic import BaseModel, ConfigDict

class Repeater_Traceback_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    enable: bool = True
    exclude_library_code: bool = True
    format_validation_error: bool = True
    record_warnings: bool = True
    traditional_stack_frame: bool = True
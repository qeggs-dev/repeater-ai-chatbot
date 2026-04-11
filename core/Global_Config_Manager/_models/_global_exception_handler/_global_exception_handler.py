from signal import Signals
from pydantic import BaseModel, ConfigDict, Field, field_validator
from ._code_reader import Code_Reader_Config
from ._repeater_traceback import Repeater_Traceback_Config

class GlobalExceptionHandlerConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    error_message: str = "Internal Server Error"
    critical_error_message: str = "Critical Server Error!"
    crash_exit: bool = True
    crash_exit_signal: int | str = "SIGINT"
    traceback_save_to: str | None = None
    record_all_exceptions: bool = False
    error_output_include_traceback: bool = False
    repeater_traceback: Repeater_Traceback_Config = Field(default_factory=Repeater_Traceback_Config)
    code_reader: Code_Reader_Config = Field(default_factory=Code_Reader_Config)

    @field_validator("crash_exit_signal")
    def validate_crash_exit_signal(cls, v: int | str):
        if isinstance(v, int):
            return v
        elif isinstance(v, str):
            for signal in Signals:
                if signal.name == v:
                    return signal.value
            raise ValueError(f"Invalid signal name: {v}")
        else:
            raise ValueError(f"Invalid type for crash_exit_signal: {type(v)}")
from pydantic import BaseModel, ConfigDict, Field
from ._code_reader import Code_Reader_Config
from ._repeater_traceback import Repeater_Traceback_Config

class Global_Exception_Handler_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    error_message: str = "Internal Server Error"
    critical_error_message: str = "Critical Server Error!"
    crash_exit: bool = True
    traceback_save_to: str | None = None
    record_all_exceptions: bool = False
    error_output_include_traceback: bool = False
    repeater_traceback: Repeater_Traceback_Config = Field(default_factory=Repeater_Traceback_Config)
    code_reader: Code_Reader_Config = Field(default_factory=Code_Reader_Config)

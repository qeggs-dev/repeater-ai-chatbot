from pydantic import BaseModel, ConfigDict

class Server_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    host: str | None = None
    port: int | None = None
    workers: int | None = None
    reload: bool | None = None
    error_message: str = "Internal Server Error"
    critical_error_message: str = "Critical Server Error!"
    crash_exit: bool = True
    traceback_save_to: str | None = None
    error_output_include_traceback: bool = False
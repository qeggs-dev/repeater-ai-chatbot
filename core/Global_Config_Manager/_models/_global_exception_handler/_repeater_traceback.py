from pydantic import BaseModel, ConfigDict

class Repeater_Traceback_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    enable: bool = True
    exclude_library_code: bool = False
    read_last_frame_only: bool = False
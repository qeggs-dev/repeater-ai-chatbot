from pydantic import BaseModel, ConfigDict

class Code_Reader_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    enable: bool = True
    code_encoding: str = "utf-8"
    code_line_dilation: int = 3
    with_numbers: bool = True
    reserve_space: int = 5
    fill_char: str = " "
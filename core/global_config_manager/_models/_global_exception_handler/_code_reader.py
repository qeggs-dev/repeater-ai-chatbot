from pydantic import BaseModel, ConfigDict, Field

class CodeReaderConfig(BaseModel):
    enable: bool = Field(default=False)
    code_encoding: str = Field(default="utf-8")
    code_line_dilation: int = Field(default=3, ge=0)
    with_numbers: bool = Field(default=True)
    reserve_space: int = Field(default=5, ge=0)
    fill_char: str = Field(default=" ")
    add_bottom_border: bool = Field(default=False)
    bottom_border_limit: int | None = Field(default=None, ge=0)
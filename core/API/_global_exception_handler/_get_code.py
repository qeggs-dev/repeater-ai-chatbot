import aiofiles

from os import PathLike
from ...Global_Config_Manager import ConfigManager

async def get_code_async(file_path: str | PathLike, line: int, dilation: int | None = None, with_numbers: bool | None = None, reserve_space: bool | None = None, fill_char: str | None = None) -> str:
    text_buffer: list[str] = []
    dilation = ConfigManager.get_configs().global_exception_handler.code_reader.code_line_dilation if dilation is None else dilation
    async with aiofiles.open(
        file_path,
        mode="r",
        encoding=ConfigManager.get_configs().global_exception_handler.code_reader.code_encoding
    ) as f:
        index: int = 0
        async for line_text in (f):
            if abs(index - line + 1) <= dilation:
                with_numbers = ConfigManager.get_configs().global_exception_handler.code_reader.with_numbers if with_numbers is None else with_numbers
                if with_numbers:
                    reserve_space = ConfigManager.get_configs().global_exception_handler.code_reader.reserve_space if reserve_space is None else reserve_space
                    fill_char = ConfigManager.get_configs().global_exception_handler.code_reader.fill_char if fill_char is None else fill_char
                    index_char = str(index + 1).rjust(reserve_space, fill_char)
                    if index + 1 == line:
                        if index_char.startswith(fill_char):
                            index_char = f">{index_char[1:]}"
                        else:
                            index_char = f">{index_char}"
                    text_buffer.append(
                        f"{index_char}| {line_text}"
                    )
                else:
                    text_buffer.append(line_text)
            
            if (index - line + 1) > dilation:
                break
            index += 1

    return "".join(text_buffer)
                
def get_code(file_path: str | PathLike, line: int, dilation: int | None = None, with_numbers: bool | None = None, reserve_space: bool | None = None, fill_char: str | None = None) -> str:
    text_buffer: list[str] = []
    dilation = ConfigManager.get_configs().global_exception_handler.code_reader.code_line_dilation if dilation is None else dilation
    with open(
        file_path,
        mode="r",
        encoding=ConfigManager.get_configs().global_exception_handler.code_reader.code_encoding
    ) as f:
        for index, line_text in enumerate(f):
            if abs(index - line + 1) <= dilation:
                with_numbers = ConfigManager.get_configs().global_exception_handler.code_reader.with_numbers if with_numbers is None else with_numbers
                if with_numbers:
                    reserve_space = ConfigManager.get_configs().global_exception_handler.code_reader.reserve_space if reserve_space is None else reserve_space
                    fill_char = ConfigManager.get_configs().global_exception_handler.code_reader.fill_char if fill_char is None else fill_char
                    index_char = str(index + 1).rjust(reserve_space, fill_char)
                    if index + 1 == line:
                        if index_char.startswith(fill_char):
                            index_char = f">{index_char[1:]}"
                        else:
                            index_char = f">{index_char}"
                    text_buffer.append(
                        f"{index_char}| {line_text}"
                    )
                else:
                    text_buffer.append(line_text)
            
            if abs(index - line + 1) > dilation:
                break

    return "".join(text_buffer)
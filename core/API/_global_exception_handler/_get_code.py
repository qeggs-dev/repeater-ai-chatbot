import aiofiles

from os import PathLike
from ...Global_Config_Manager import ConfigManager
from typing import Generator, Iterable

class GetCode:
    def __init__(
            self,
            file_path: str | PathLike,
            line: int,
            dilation: int | None = None,
            with_numbers: bool | None = None,
            reserve_space: bool | None = None,
            fill_char: str | None = None
        ):
        self._file_path = file_path
        self._line = line
        self._dilation = dilation
        self._with_numbers = with_numbers
        self._reserve_space = reserve_space
        self._fill_char = fill_char

    async def get_code_async(self) -> str:
        text_buffer: list[str] = []
        dilation = ConfigManager.get_configs().global_exception_handler.code_reader.code_line_dilation if self._dilation is None else self._dilation
        async with aiofiles.open(
            self._file_path,
            mode="r",
            encoding=ConfigManager.get_configs().global_exception_handler.code_reader.code_encoding
        ) as f:
            index: int = 0
            async for self._line in f:
                processed_text = self._get_line_text(
                    text=self._line,
                    index=index,
                )
                if isinstance(processed_text, str):
                    text_buffer.append(processed_text)
                if (index - self._line + 1) > dilation:
                    break
        
        return "".join(text_buffer)
                    
    def get_code(self) -> str:
        text_buffer: list[str] = []
        dilation = ConfigManager.get_configs().global_exception_handler.code_reader.code_line_dilation if self._dilation is None else self._dilation
        with open(
            self._file_path,
            mode="r",
            encoding=ConfigManager.get_configs().global_exception_handler.code_reader.code_encoding
        ) as f:
            for index, self._line in enumerate(f):
                processed_text = self._get_line_text(
                    text=self._line,
                    index=index,
                )
                if isinstance(processed_text, str):
                    text_buffer.append(processed_text)
                if (index - self._line + 1) > dilation:
                    break

        return "".join(text_buffer)
    
    def _get_line_text(
            self,
            text: str,
            index: int,
        ) -> str | None:

        if abs(index - self._line + 1) <= self._dilation:
            if self._with_numbers is None:
                with_numbers = ConfigManager.get_configs().global_exception_handler.code_reader.with_numbers
            else:
                with_numbers = self._with_numbers
            
            if with_numbers:
                if self._reserve_space is None:
                    reserve_space = ConfigManager.get_configs().global_exception_handler.code_reader.reserve_space
                else:
                    reserve_space = self._reserve_space

                if self._fill_char is None:
                    fill_char = ConfigManager.get_configs().global_exception_handler.code_reader.fill_char
                else:
                    fill_char = self._fill_char
                
                index_char = str(index + 1).rjust(reserve_space, fill_char)
                if index + 1 == self._line:
                    if index_char.startswith(fill_char):
                        index_char = f">{index_char[1:]}"
                    else:
                        index_char = f">{index_char}"
                return f"|{index_char}| {text}"
            else:
                return text
        return None
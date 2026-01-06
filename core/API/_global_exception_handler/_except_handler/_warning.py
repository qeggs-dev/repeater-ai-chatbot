import warnings
import aiofiles

from typing import TextIO
from loguru import logger
from datetime import datetime
from pathlib import Path

from ....Global_Config_Manager import ConfigManager
from .._get_code import get_code

class WarningHandler:
    """Warning Handler"""
    def __init__(self) -> None:
        self.raw_showwarning = warnings.showwarning
    
    def inject(self) -> None:
        warnings.showwarning = self.warning_handler
    
    def remove(self) -> None:
        warnings.showwarning = self.raw_showwarning
    
    def warning_handler(
            self,
            message: Warning | str,
            category: type[Warning],
            filename: str,
            lineno: int,
            file: TextIO | None = None,
            line: str | None = None
        ) -> None:
        if ConfigManager().get_configs().global_exception_handler.record_warnings:
            warning_time = datetime.now()
            file_path = Path(filename)

            if ConfigManager().get_configs().global_exception_handler.code_reader.enable:
                code = get_code(file_path, lineno)

            # 记录异常日志
            logger.warning(
                (
                    "Warning: \n"
                    "{warning_name}\n"
                    "    - Raised from:\n"
                    "        {raiser}:{lineno}\n"
                    "    - Message: \n"
                    "        {message}\n"
                    "File: \n"
                    "{code}"
                ),
                user_id = "[Global Exception Recorder]",
                warning_name = category.__name__,
                message = message,
                raiser = file_path.as_posix(),
                lineno = lineno,
                code = code
            )
        else:
            self.raw_showwarning(
                message = message,
                category = category,
                filename = filename,
                lineno = lineno,
                file = file,
                line = line
            )
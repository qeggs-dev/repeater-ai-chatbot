import warnings
import aiofiles

from typing import TextIO
from loguru import logger
from datetime import datetime
from pathlib import Path

from ....Global_Config_Manager import ConfigManager
from .._get_code import get_code

def warning_handler(
        message: Warning | str,
        category: type[Warning],
        filename: str,
        lineno: int,
        file: TextIO | None = None,
        line: str | None = None
    ) -> None:
    warning_time = datetime.now()
    file_path = Path(filename)

    if ConfigManager().get_configs().global_exception_handler.code_reader.enable:
        code = get_code(file_path, lineno)

    # 记录异常日志
    logger.warning(
        (
            "Warning: \n"
            "    - Type: \n"
            "        {warning_name}\n"
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

warnings.showwarning = warning_handler
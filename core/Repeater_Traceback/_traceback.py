import os
import sys
import json
import traceback

from ._get_code import GetCode
from pathlib import Path
from typing import Generator
from pydantic import ValidationError
from ..text_buffer import TextBuffer, IndentedText

class TracebackHandler:
    @staticmethod
    def is_library_code(filename: str | os.PathLike):
        if not filename:
            return True
        
        file_path = Path(filename)
        file_name_str = str(filename)
        
        stdlib_dirs: list[str] = [
            sys.prefix,
            sys.base_prefix,
        ]
        stdlib_dirs: list[Path] = [Path(dir) for dir in stdlib_dirs]
        for dir in stdlib_dirs.copy():
            stdlib_dirs.append(dir / "lib")
        
        for lib_dir in stdlib_dirs:
            if file_path.is_relative_to(lib_dir):
                return True
        
        for path in sys.path:
            if "site-packages" in path and file_name_str.startswith(path):
                return True
            if "dist-packages" in path and file_name_str.startswith(path):
                return True
        
        if file_name_str.startswith("<") and file_name_str.endswith(">"):
            return True
        
        return False

    def format_stack_frame(self, frames: traceback.StackSummary, exclude_library: bool = False) -> Generator[str, None, None]:
        for index, frame in enumerate(frames):
            text_buffer = TextBuffer()
            file_path = Path(frame.filename)
            if self.is_library_code(file_path):
                frame_flag = "Library Code"
                if exclude_library:
                    text_buffer.push_single_no_conversion(
                        f"[{index}] Frame ({frame_flag}): {file_path.as_posix()}:{frame.lineno}"
                    )
                    continue
            else:
                frame_flag = "App Code"
            
            text_buffer.push_single_no_conversion(
                f"[{index}] Frame ({frame_flag}): {file_path.as_posix()}:{frame.lineno}"
            )
            text_buffer.push_single(
                IndentedText(
                    f"- Function: {frame.name}",
                    f"- Line: {frame.lineno} ~ {frame.end_lineno}",
                    f"- Columns: {frame.colno} ~ {frame.end_colno}",
                    f"- Locals:",
                    indent_level = 2
                )
            )
            text_buffer.push_single(
                IndentedText(
                    json.dumps(frame.locals, indent=4, ensure_ascii=False),
                    indent_level = 4
                )
            )
            yield str(text_buffer)
            
    
    @staticmethod
    async def code_reader(
            raiser: Path,
            frame: traceback.FrameSummary,
            enable_code_reader: bool = True
        ) -> str:
        if enable_code_reader:
            if raiser.exists() and raiser.is_file() and frame.lineno is not None and frame.lineno > 0:
                get_code = GetCode(
                    raiser,
                    frame.lineno,
                    frame.end_lineno,
                    frame.colno,
                    frame.end_colno
                )
                try:
                    code = await get_code.get_code_async()
                except Exception as e:
                    code = f"[Get Code Error: {e}]"
            else:
                code = "[Invalid Code Frame]"
        else:
            code = "[Code Reader Disabled]"
        return code
        

    async def format_traceback(
            self,
            time_str: str,
            exclude_library: bool = False,
            enable_code_reader: bool = False,
            traditional_stack_frame: bool = False,
            format_validation_error: bool = False,
        ):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        frames = traceback.extract_tb(exc_traceback)
        last_frame = frames[-1]
        last_self_frame: traceback.FrameSummary | None = None
        for frame in reversed(frames):
            if not self.is_library_code(frame.filename):
                last_self_frame = frame
                break
        total_frame_depth = len(frames)
        raiser = Path(last_frame.filename)
        last_self_raiser = None
        for frame in reversed(frames):
            if not self.is_library_code(frame.filename):
                last_self_raiser = frame
                break
        line_start = last_frame.lineno
        line_end = last_frame.end_lineno
        column_start = last_frame.colno
        column_end = last_frame.end_colno
        error_name = exc_value.__class__.__name__

        if format_validation_error and isinstance(exc_value, ValidationError):
            text_buffer = TextBuffer(separator="\n")
            errors = exc_value.errors()
            for error in errors:
                text_buffer.push_single_no_conversion(f"{'.'.join(error['loc'])} - {error['msg']}")
            message = str(text_buffer)
        else:
            message = str(exc_value)

        indented_message = IndentedText(
            message,
            indent_level = 4,
            first_line_indent = False
        )
        if traditional_stack_frame:
            traceback_str = traceback.format_exc()
        else:
            traceback_str = "\n".join(self.format_stack_frame(frames, exclude_library))
        indented_traceback = IndentedText(
            traceback_str,
            indent_level = 4,
            first_line_indent = False
        )

        if last_self_raiser and last_self_frame:
            code = await self.code_reader(
                raiser = last_self_raiser,
                frame = last_self_frame,
                enable_code_reader = enable_code_reader,
            )
        else:
            code = await self.code_reader(
                raiser = raiser,
                frame = last_frame,
                enable_code_reader = enable_code_reader,
            )
        
        format_texts: TextBuffer = TextBuffer(separator = "\n")
        format_texts.push_no_conversion(
            f"{error_name}",
            "  - Time:",
            f"    {time_str}",
            "  - Depth of stack frame:",
            f"    {total_frame_depth}",
            "  - Raised:",
            "    - Path:",
            f"      {raiser.as_posix()}:{line_start}:{column_start}",
            "    - Line Range:",
            f"      {line_start} ~ {line_end}",
            "    - Column Range:",
            f"      {column_start} ~ {column_end}",
            "  - Message:",
            f"    {indented_message}",
            "  - Traceback:",
            f"    {indented_traceback}",
        )
        if enable_code_reader:
            format_texts.push_no_conversion(
                "File Context:",
                code
            )
        
        format_texts.push_empty()
        format_texts.push_no_conversion(
            f"{error_name}:",
            message,
        )
        format_texts.push_empty()
        
        return str(format_texts)
        
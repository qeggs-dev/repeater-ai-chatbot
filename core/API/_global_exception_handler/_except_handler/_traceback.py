import os
import sys
import traceback

from pathlib import Path

from .._get_code import get_code_async

def is_library_code(filename: str):
    if not filename:
        return True
    
    file_path = Path(filename)
    
    stdlib_dirs: list[str] = [
        sys.prefix,
        sys.base_prefix,
    ]
    stdlib_dirs: list[Path] = [Path(dir) for dir in stdlib_dirs]
    for dir in stdlib_dirs.copy():
        stdlib_dirs.append(dir / 'lib')
    
    for lib_dir in stdlib_dirs:
        if file_path.is_relative_to(lib_dir):
            return True
    
    for path in sys.path:
        if 'site-packages' in path and filename.startswith(path):
            return True
        if 'dist-packages' in path and filename.startswith(path):
            return True
    
    if filename.startswith('<') and filename.endswith('>'):
        return True
    
    return False

async def format_traceback(exclude_library_code: bool = False, read_last_frame_only: bool = False):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    text_buffer: list[str] = []
    text_buffer.append("Traceback:")
    frames = traceback.extract_tb(exc_traceback)
    for index, frame in enumerate(frames):
        if is_library_code(frame.filename):
            frame_flag = "Library Code"
            if exclude_library_code:
                text_buffer.append(f"[{index}] Frame ({frame_flag})")
                continue
        else:
            frame_flag = "App Code"
        
        text_buffer.append(
            f"[{index}] Frame ({frame_flag}):\n"
            f"    - File:\n"
            f"        {frame.filename}:{frame.lineno}\n"
            f"    - Line:\n"
            f"        {frame.lineno}\n"
            f"    - Function:\n"
            f"        {frame.name}"
        )

        if not read_last_frame_only or index == len(frames) - 1:
            text_buffer.append(
                f"    - Code:\n"
                f"        {await get_code_async(frame.filename, frame.lineno).replace('\n', '\n        |')}"
            )
    text_buffer.append(f"Exception: {exc_type.__name__}")
    text_buffer.append(f"Message: \n{exc_value}")
    return "\n".join(text_buffer)
    
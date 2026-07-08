import numpy as np

from typing import Generator
from ..assist import min_max_normalize

def draw_chart(data: np.ndarray[tuple[int]], title: str, height: int = 5) -> Generator[str, None, None]:
    """绘制图表"""
    assert isinstance(data, np.ndarray), "data Must be a numpy array"
    assert isinstance(title, str), "title Must be a string"
    assert isinstance(height, int) and height > 0, "height Must be a positive integer"

    if len(data) == 0:
        yield "No Data"
        return
    zoomed_data = min_max_normalize(data) * height
    ctitle = f" {title} ".center(len(zoomed_data) + 2, "─")
    yield f"┌{ctitle}┐"
    for i in range(height - 1, -1, -1):
        text_buffer: list[str] = []
        for j in zoomed_data:
            if j - i > 1:
                text_buffer.append("█")
            elif j - i > 0.75:
                text_buffer.append("▓")
            elif j - i > 0.5:
                text_buffer.append("▒")
            elif j - i > 0.25:
                text_buffer.append("░")
            else:
                text_buffer.append(" ")
        
        charts = "".join(text_buffer)
        yield f"│ {charts} │"
    end_line = "─" * (len(zoomed_data) + 2)
    yield f"└{end_line}┘"
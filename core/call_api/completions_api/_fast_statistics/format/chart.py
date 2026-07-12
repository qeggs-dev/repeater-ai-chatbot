import numpy as np

from typing import Generator
from ..assist import min_max_normalize, sample

def draw_chart(
        data: np.ndarray[tuple[int]],
        title: str,
        width: int = 10,
        height: int = 5
    ) -> Generator[str, None, None]:
    """绘制图表"""
    if len(data) == 0:
        yield "No Data"
        return
    
    if width < 5 or height < 3:
        raise ValueError("width and height must be greater than 5 and 3")
    
    draw_width = width - 4
    draw_height = height - 2

    sampled_data = sample(data, draw_width)

    zoomed_data = min_max_normalize(sampled_data) * draw_height
    ctitle = f" {title} ".center(draw_width + 2, "─")
    yield f"┌{ctitle}┐"
    for i in range(height - 3, -1, -1):
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
        
        chart_str = "".join(text_buffer)
        fill_space = " " * (width - 4 - len(chart_str))
        yield f"│ {chart_str}{fill_space} │"
    end_line = "─" * (draw_width + 2)
    yield f"└{end_line}┘"
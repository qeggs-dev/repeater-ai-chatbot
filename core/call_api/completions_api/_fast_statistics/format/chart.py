import numpy as np

from typing import Any, Generator, Iterable
from .....auxiliary.type_checker import is_iterable
from ..assist import min_max_normalize, sample

class Chart:
    def __init__(
        self,
        title: str,
        data: np.ndarray,
    ):
        self.title = title
        self.data = data
        self._no_drawing = False
        if len(self.data.shape) != 1:
            raise ValueError("data must be 1-dimensional")
        
        elif len(self.data) == 0:
            self._no_drawing = True
        
        elif np.isnan(self.data).any():
            raise ValueError("data must not contain NaN values")
        
        elif (np.max(self.data) - np.min(self.data)) == 0:
            self._no_drawing = True
    
    def draw(
        self,
        width: int = 10,
        height: int = 5,
    ) -> str:
        return "\n".join(
            self.draw_lines(
                width,
                height
            )
        )
    
    def draw_lines(
        self,
        width: int = 10,
        height: int = 5
    ) -> Generator[str, None, None]:
        if width < 5 or height < 3:
            raise ValueError("width and height must be greater than 5 and 3")
        
        if self._no_drawing:
            return self._draw_framewark(
                "",
                width,
                height
            )
        else:
            return self._draw_framewark(
                (line for line in
                    self._draw_chart(
                        width - 4,
                        height - 2
                    )
                ),
                width,
                height
            )
    
    def _draw_chart(
        self,
        width: int = 10,
        height: int = 5
    ) -> list[str]:
        sampled_data = sample(self.data, width)
        zoomed_data = min_max_normalize(sampled_data) * height
        
        levels = np.arange(height - 1, -1, -1).reshape(-1, 1)
        diff = zoomed_data.reshape(1, -1) - levels
        
        thresholds = np.array([-np.inf, 0.25, 0.5, 0.75, 1.0, np.inf])
        chars = np.array([' ', '░', '▒', '▓', '█'])
        
        indices = np.digitize(diff, thresholds) - 1
        indices = np.clip(indices, 0, 4)
        
        char_matrix = chars[indices]
        lines = [''.join(row) for row in char_matrix]
        
        return lines
    
    def _draw_framewark(
        self,
        text: str | Iterable[str],
        width: int = 10,
        height: int = 5,
    ) -> Generator[str, None, None]:
        
        ctitle = f" {self.title} ".center(width - 2, "─")
        yield f"┌{ctitle}┐"

        if isinstance(text, str):
            text_iter = iter(text.splitlines())
        elif is_iterable(text):
            text_iter = iter(text)
        else:
            raise TypeError("text must be a string or an iterable of strings")
        
        lines: list[str] = []
        max_len: int = 0
        
        for line in text_iter:
            lines.append(line)
            max_len = max(max_len, len(line))

        for index, line in enumerate(lines):
            if index > height - 2:
                break
            
            if max_len < width - 4:
                yield f"│ {line.ljust(max_len)}┊{' ' * (width - 5 - max_len)} │"
            else:
                yield f"│ {line[:width - 4]} │"
        
        yield f"└{'─' * (width - 2)}┘"
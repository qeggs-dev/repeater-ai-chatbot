from typing import Generator, Any

class TextBuffer:
    """
    TextBuffer class represents a buffer for storing text.
    It provides methods for pushing, popping, merging, and clearing the buffer.
    """

    def __init__(self, *text: Any, separator: str = ""):
        """
        TextBuffer class represents a buffer for storing text.
        It provides methods for pushing, popping, merging, and clearing the buffer.

        Args:
            *text (str): The text to be stored in the buffer.
            separator (str): The separator to be used between the text elements.
        """
        self._buffer: list[str] = []
        self._separator = separator
        if text:
            self.append(*text)
    
    @property
    def separator(self) -> str:
        return self._separator
    
    def __bool__(self) -> bool:
        """Returns True if buffer contains any non-empty text (considering delimiters)."""

        # If there is nothing,
        # the delimiter output is empty even if there is one.
        if not self._buffer:
            return False
        
        # Cache results to speed up.
        length = len(self._buffer)

        # When the length is only 1,
        # directly check the first block can be.
        if length == 1:
            return bool(self._buffer[0])
        
        # If the delimiter is not empty when all fragments are empty
        # and the length is greater than 1,
        # then the string is not empty in any way.
        if self._separator and length > 1:
            return True
        
        return any(self._buffer)
    
    def __len__(self):
        """
        Return the length of the buffer.
        """
        raw_length = sum(len(text) for text in self._buffer)
        if self._separator:
            return raw_length + len(self._separator) * (len(self._buffer) - 1)
        else:
            return raw_length
    
    def __str__(self) -> str:
        """
        Return a string representation of the buffer.
        """
        return self._separator.join(self._buffer)
    
    @property
    def num_segments(self) -> int:
        """
        Return the number of text segments in the buffer.
        """
        return len(self._buffer)
    
    def merge(self) -> str:
        """
        Merge the buffer into a single string and replace the buffer with the merged string.

        Returns:
            str: The merged string
        """
        text = str(self)
        self._buffer = [text]
        return text
    
    def append(self, *text: Any):
        """
        Push a string into the buffer.

        Args:
            text (str): The string to be pushed into the buffer
        """
        for t in text:
            self._buffer.append(str(t))
    
    def push_empty(self):
        """
        Push an empty string into the buffer.
        """
        self._buffer.append("")

    def pop(self) -> str:
        """
        Pop a string from the buffer.

        Returns:
            str: The popped string
        """
        text = self._buffer.pop()
        return text
    
    def clear(self):
        """
        Clear the buffer.
        """
        self._buffer.clear()
    
    def copy(self) -> "TextBuffer":
        """
        Copy the buffer.

        Returns:
            TextBuffer: The copied buffer
        """
        buffer = TextBuffer(
            *self._buffer,
            separator = self._separator
        )
        return buffer
    
    def __iter__(self) -> Generator[str, None, None]:
        """
        Iterate over the buffer.

        Yields:
            str: Each character in the buffer
        """
        for text in self._buffer:
            for char in text:
                yield char
    
    def __add__(self, other: str | "TextBuffer") -> "TextBuffer":
        """
        Add a string or another buffer to the buffer.

        Args:
            other (str | TextBuffer): The string or buffer to add

        Returns:
            TextBuffer: The resulting buffer
        """
        buffer = self.copy()
        if isinstance(other, str):
            buffer.append(other)
            return buffer
        elif isinstance(other, TextBuffer):
            buffer._buffer.extend(other._buffer)
            return buffer
        else:
            return NotImplemented
        

    def __iadd__(self, other: str | "TextBuffer") -> "TextBuffer":
        """
        Add a string or another buffer to the buffer in-place.

        Args:
            other (str | TextBuffer): The string or buffer to add

        Returns:
            TextBuffer: The resulting buffer
        """
        if isinstance(other, str):
            self.append(other)
            return self
        elif isinstance(other, TextBuffer):
            self._buffer.extend(other._buffer)
            return self
        else:
            return NotImplemented
    
    def __radd__(self, other: str | "TextBuffer") -> "TextBuffer":
        """
        Add a string or another buffer to the buffer.

        Args:
            other (str | TextBuffer): The string or buffer to add

        Returns:
            TextBuffer: The resulting buffer
        """
        buffer = self.copy()
        if isinstance(other, str):
            buffer._buffer.insert(0, other)
            return buffer
        elif isinstance(other, TextBuffer):
            buffer._buffer = other._buffer + buffer._buffer
            return buffer
        else:
            return NotImplemented

    def __repr__(self) -> str:
        """
        Return a string representation of the buffer.

        Returns:
            str: The string representation of the buffer
        """
        args = [repr(x) for x in self._buffer]
        return f"{self.__class__.__name__}({', '.join(args)})"
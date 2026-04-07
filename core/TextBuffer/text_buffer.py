from typing import Generator

class TextBuffer:
    """
    TextBuffer class represents a buffer for storing text.
    It provides methods for pushing, popping, merging, and clearing the buffer.
    """

    def __init__(self, delimiters: str = ""):
        """
        TextBuffer class represents a buffer for storing text.
        It provides methods for pushing, popping, merging, and clearing the buffer.

        Args:
            delimiters (str, optional): A string of delimiters to be used for splitting the buffer. Defaults to "".
        """
        self._buffer: list[str] = []
        self._delimiters = delimiters
        self._length = 0
    
    def __bool__(self) -> bool:
        """Returns True if buffer contains any non-empty text (considering delimiters)."""
        if not self._buffer:
            return False
        
        if self._delimiters and len(self._buffer) > 1:
            return True
        
        return any(self._buffer)
    
    def __len__(self):
        """
        Return the length of the buffer.
        """
        return self._length
    
    def __str__(self) -> str:
        """
        Return a string representation of the buffer.
        """
        return self._delimiters.join(self._buffer)
    
    def __repr__(self) -> str:
        """
        Return a string representation of the buffer.
        """
        return f"<{self.__class__.__name__} length={self._length}>"
    
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
        self._length = len(text)
        return text
    
    def push(self, text: str):
        """
        Push a string into the buffer.

        Args:
            text (str): The string to be pushed into the buffer
        """
        self._length += len(text)
        self._buffer.append(text)

    def pop(self) -> str:
        """
        Pop a string from the buffer.

        Returns:
            str: The popped string
        """
        text = self._buffer.pop()
        self._length -= len(text)
        return text
    
    def clear(self):
        """
        Clear the buffer.
        """
        self._length = 0
        self._buffer.clear()
    
    def copy(self) -> 'TextBuffer':
        """
        Copy the buffer.

        Returns:
            TextBuffer: The copied buffer
        """
        buffer = TextBuffer(
            self._delimiters
        )
        for text in self._buffer:
            buffer.push(text)
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
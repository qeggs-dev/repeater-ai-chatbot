from typing import Generator, Iterable, Any, overload

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
        self.consume_iterable(text)
    
    @property
    def separator(self) -> str:
        """
        The separator used between the text elements.
        """
        return self._separator
    
    @separator.setter
    def separator(self, value: str) -> None:
        self._separator = str(value)
    
    def __bool__(self) -> bool:
        """
        Returns True if buffer contains any non-empty text (considering delimiters).
        """

        # If there is nothing,
        # the delimiter output is empty even if there is one.
        if not self._buffer:
            return False

        # When the length is only 1,
        # directly check the first block can be.
        if len(self._buffer) == 1:
            return bool(self._buffer[0])
        
        # If the delimiter is not empty when all fragments are empty
        # and the length is greater than 1,
        # then the string is not empty in any way.
        if self._separator and len(self._buffer) > 1:
            return True
        
        return any(self._buffer)
    
    @overload
    def __getitem__(self, index: int) -> str:
        ...
    
    @overload
    def __getitem__(self, index: slice) -> list[str]:
        ...
    
    def __getitem__(self, index: int | slice) -> str | list[str]:
        """
        Returns the text at the specified index or slice.
        """
        return self._buffer[index]
    
    @overload
    def __setitem__(self, index: int, value: str) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[str]) -> None:
        ...

    def __setitem__(self, index: int | slice, value: str | Iterable[str]) -> None:
        """
        Sets the text at the specified index.
        """
        if isinstance(index, int):
            self._buffer[index] = value
        elif isinstance(index, slice):
            self._buffer[index] = [str(v) for v in value]

    def __delitem__(self, index: int) -> None:
        del self._buffer[index]
    
    @property
    def is_empty(self) -> bool:
        """Check if the buffer would produce an empty string."""
        return not bool(self)
    
    def __len__(self):
        """
        Return the number of substrings in the buffer.
        """
        return len(self._buffer)
    
    def str_length(self) -> int:
        """
        Return the length of the buffer as a string.
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
    
    def consume_iterable(self, iterable: Iterable[Any]) -> None:
        """
        Consume an iterable and append each item to the buffer.

        Args:
            generator (Iterable[Any]): The iterable to consume.
        """
        self._buffer.extend(str(item) for item in iterable)
    
    def consume_iterable_no_conversion(self, iterable: Iterable[str]) -> None:
        """
        Consume an iterable and append each item without converting to a string.

        Args:
            generator (Iterable[Any]): The iterable to consume.
        """
        self._buffer.extend(iterable)
    
    def push(self, *text: Any):
        """
        Push a string into the buffer.

        Args:
            text (str): The string to be pushed into the buffer
        """
        self.consume_iterable(text)
    
    def push_single(self, text: Any):
        """
        Push a single string into the buffer.

        Args:
            text (str): The string to be pushed into the buffer
        """
        if not isinstance(text, str):
            text = str(text)
        self._buffer.append(text)
    
    def push_single_no_conversion(self, text: str):
        """
        Push a string into the buffer without converting it to a string.

        Args:
            text (str): The string to be pushed into the buffer
        """
        self._buffer.append(text)
    
    def write(self, text: str) -> int:
        """
        **Stringio compatibility interface.**

        Write a string into the buffer.

        Args:
            text (str): The string to be written into the buffer

        Returns:
            int: The number of characters written
        """
        if not isinstance(text, str):
            raise TypeError(f"string argument expected, got '{type(text).__name__}'")
        self._buffer.append(text)
        return len(text)

    def getvalue(self) -> str:
        """
        **Stringio compatibility interface.**

        Return the buffer as a string.

        Returns:
            str: The buffer as a string
        """
        return str(self)
    
    def append(self, text: str) -> None:
        """
        **list[str] compatibility interface.**

        Append a string into the buffer.

        Args:
            text (str): The string to be appended into the buffer
        """
        if not isinstance(text, str):
            text = str(text)
        self._buffer.append(text)
    
    def push_empty(self, n: int = 1) -> None:
        """
        Push an empty string into the buffer.
        """
        self._buffer.extend([""] * n)

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
            str: The string in the buffer
        """
        for text in self._buffer:
            yield text
    
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
            buffer.push(other)
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
            self.push(other)
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
        if isinstance(other, str):
            buffer = self.copy()
            buffer._buffer.insert(0, other)
            return buffer
        elif isinstance(other, TextBuffer):
            buffer = other.copy()
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
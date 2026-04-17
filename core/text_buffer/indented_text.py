class IndentedText:
    def __init__(
            self,
            *texts: str,
            indent_level: int = 0,
            separator: str = "\n",
            indent_str: str = " ",
            first_line_indent: bool = True
        ):
        self.texts = texts
        self.indent_level: int = indent_level
        self.separator = separator
        self.indent_str = indent_str
        self.first_line_indent = first_line_indent

    @property
    def full_text(self) -> str:
        return self.separator.join(self.texts)
    
    @property
    def _indent_string(self) -> str:
        return self.indent_str * self.indent_level

    def to_indented_text(self) -> str:
        indent = self._indent_string
        indented_text = self.full_text.replace("\n", "\n" + indent)
        if self.first_line_indent:
            indented_text = indent + indented_text
        return indented_text
    
    def __str__(self) -> str:
        return self.to_indented_text()
from ..text import format_carry_duration

TOKEN_LEVELS = [
    ("token", "", 1024),
    ("K token", "K", 1024),
    ("M token", "M", 1024),
    ("G token", "G", 1024),
    ("T token", "T", 1024),
    ("P token", "P", 1024),
]

def format_token_duration(duration: int, start_with: int = 0, use_abbreviation: bool = False, delimiter: str = ", ") -> str:
    return format_carry_duration(
        value = duration,
        start_with = start_with,
        levels = TOKEN_LEVELS,
        use_abbreviation = use_abbreviation,
        delimiter = delimiter,
        final_level = ("E tokens", "E"),
    )
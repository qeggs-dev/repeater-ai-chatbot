from ..text import format_carry_duration

TOKEN_LEVELS = [
    ("Tokens", "", 1024),
    ("K Tokens", "K", 1024),
    ("M Tokens", "M", 1024),
    ("G Tokens", "G", 1024),
    ("T Tokens", "T", 1024),
    ("P Tokens", "P", 1024),
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
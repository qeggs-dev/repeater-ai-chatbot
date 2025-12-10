from TextProcessors import format_carry_duration

TIME_LEVELS: list[tuple[str, str, int]] = [
    ("nanosecond", "ns", 1000),
    ("microsecond", "μs", 1000),
    ("millisecond", "ms", 1000),
    ("second", "s", 60),
    ("minute", "min", 60),
    ("hour", "h", 24),
    ("day", "day", 30),
    ("month", "mon", 12),
    ("year", "y", 100),
]

def format_time_duration(duration: int, start_with: int = 0, use_abbreviation: bool = False, delimiter: str = ", ") -> str:
    """
    Format time duration in nanoseconds to a human-readable string.
    """
    return format_carry_duration(
        value=duration,
        levels=TIME_LEVELS,
        start_with=start_with,
        use_abbreviation=use_abbreviation,
        delimiter=delimiter,
        final_level=("century", "cent")
    )
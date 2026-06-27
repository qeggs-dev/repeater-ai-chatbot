from ..text import format_carry_duration

NS_TIME_LEVELS: list[tuple[str, str, int]] = [
    ("nanosecond", "ns", 1000),
    ("microsecond", "μs", 1000),
    ("millisecond", "ms", 1000),
    ("second", "s", 60),
    ("minute", "min", 60),
    ("hour", "h", 24),
    ("day", "day", 30),
    ("month", "mon", 12),
    ("year", "y", 10),
    ("decade", "dec", 10),
    ("century", "cent", 10),
]

TIME_LEVELS: list[tuple[str, str, int]] = [
    ("second", "s", 60),
    ("minute", "min", 60),
    ("hour", "h", 24),
    ("day", "day", 30),
    ("month", "mon", 12),
    ("year", "y", 100),
]

def format_time_duration_ns(duration: int | float, start_with: int = 0, use_abbreviation: bool = False, delimiter: str = ", ") -> str:
    """
    Format time duration in nanoseconds to a human-readable string.
    """
    return format_carry_duration(
        value=duration,
        levels=NS_TIME_LEVELS,
        start_with=start_with,
        use_abbreviation=use_abbreviation,
        delimiter=delimiter,
        final_level=("century", "cent")
    )

def format_time_duration(duration: int | float, start_with: int = 0, use_abbreviation: bool = False, delimiter: str = ", ") -> str:
    """
    Format time duration in seconds to a human-readable string.
    """
    return format_carry_duration(
        value=duration,
        levels=TIME_LEVELS,
        start_with=start_with,
        use_abbreviation=use_abbreviation,
        delimiter=delimiter,
        final_level=("millennium", "mill")
    )
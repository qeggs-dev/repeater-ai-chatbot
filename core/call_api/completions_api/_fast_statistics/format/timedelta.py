from .....auxiliary.time import format_time_duration_ns

def format_timedelta(
    timedelta: int | float,
) -> str:
    assert isinstance(timedelta, (int, float)), "timedelta must be an int or float"
    return f"{timedelta / 1e6:.2f}ms({format_time_duration_ns(timedelta, use_abbreviation=True)})"
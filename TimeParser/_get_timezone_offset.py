from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

def get_timezone_offset(
        timezone: str | ZoneInfo,
        dt: datetime | None = None,
    )  -> timedelta:
    """
    Get the timezone offset in seconds for a given timezone and datetime.

    Args:
        timezone (str | ZoneInfo): The timezone to get the offset for.
        dt (datetime | None): The datetime to get the offset for. If None, the current time is used.

    Returns:
        int: The timezone offset in seconds.
    """
    if dt is None:
        dt = datetime.now()
    
    if isinstance(timezone, str):
        timezone = ZoneInfo(timezone)
    elif not isinstance(timezone, ZoneInfo):
        raise TypeError("timezone must be a str or ZoneInfo object")

    offset = timezone.utcoffset(dt)
    if offset is None:
        return timedelta()
    return offset


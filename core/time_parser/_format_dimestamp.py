from datetime import datetime, timezone, timedelta

def tz_timestamp(timestamp: float | datetime, offset_timezone: timedelta) -> datetime:
    """
    转换时间戳为指定时区的日期时间
    
    参数:
        timestamp (float | datetime): 时间戳（秒数，可以是整数或浮点数）
        offset_timezone (timedelta): 时区偏移量
    
    返回:
        datetime: 指定时区的日期时间
    """
    # 创建固定偏移的时区
    custom_tz = timezone(offset_timezone)
    
    # 将时间戳转换为带时区信息的datetime对象
    if isinstance(timestamp, datetime):
        utc_time = timestamp.astimezone(timezone.utc)
    elif isinstance(timestamp, float) or isinstance(timestamp, int):
        utc_time = datetime.fromtimestamp(timestamp, timezone.utc)
    else:
        raise TypeError("timestamp must be a datetime object or a timestamp")
    local_time = utc_time.astimezone(custom_tz)
    
    return local_time
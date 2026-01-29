from datetime import datetime, timedelta

def calculate_age(
        birth_year: int,
        birth_month: int,
        birth_day: int,
        current_timestamp: datetime = None,
        offset_timezone: timedelta = timedelta()
    ):
    """
    计算一个人的年龄（整型）
    
    Args:
        birth_year: 出生年份
        birth_month: 出生月份
        birth_day: 出生日
        current_timestamp: 时间（可选，默认为当前系统时间）
        offset_timezone: 时区偏移量（小时，可选，默认为0）
    
    Returns:
        年龄（整型）
    """
    if current_timestamp is None:
        base_time = datetime.now()
    else:
        base_time = current_timestamp
    
    base_time = base_time + offset_timezone

    age = base_time.year - birth_year
    
    # 如果今年还没过生日，年龄减1
    if (base_time.month, base_time.day) < (birth_month, birth_day):
        age -= 1
    return age

def calculate_precise_age(
        birth_year: int,
        birth_month: int,
        birth_day: int,
        birth_hour: int | None = None,
        birth_minute: int | None = None,
        birth_second: int | None = None,
        current_timestamp: datetime = None,
        offset_timezone: timedelta = timedelta()
    ) -> float:
    """
    计算一个人的年龄（浮点型）
    
    Args:
        birth_year (int): 出生日期的年份
        birth_month (int): 出生日期的月份
        birth_day (int): 出生日期的日期
        current_timestamp (datetime, optional): 当前时间戳. Defaults to None.
        offset_timezone (timedelta, optional): 时区偏移量. Defaults to timedelta().

    Returns:
        float: 年龄（浮点型）
    """
    if current_timestamp is None:
        base_time = datetime.now()
    else:
        base_time = current_timestamp
    

    birthday = datetime(
        birth_year,
        birth_month,
        birth_day,
        birth_hour or 0,
        birth_minute or 0,
        birth_second or 0
    )

    delta = base_time - birthday

    return delta.total_seconds() / 3600 / 24 / 365.25
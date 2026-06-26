from datetime import datetime, timedelta, timezone

def calculation_date_countdown(
        target_month: int,
        target_day: int,
        target_hour: int | None = None,
        target_minute: int | None = None,
        target_second: int | None = None,
        current_timestamp: datetime | None = None,
        tz_offset: timezone | None = None,
) -> timedelta:
    """
    获取距离目标日期还有多少天/时间
    
    参数:
        target_month: 目标月份 (1-12)
        target_day: 目标日期 (1-31)
        target_hour: 目标小时 (0-23)，默认为0
        target_minute: 目标分钟 (0-59)，默认为0
        target_second: 目标秒数 (0-59)，默认为0
        current_timestamp: 当前时间，默认为当前系统时间
        tz_offset: 时区偏移，默认使用当前时间的时区
    
    返回:
        timedelta: 距离目标时间的时间差
    
    注意:
        - 如果目标日期在当年已过，则计算到下一年的目标日期
        - 非闰年的2月29日会被当作3月1日处理
        - 返回的时间差包含时分秒，不只是一整天
    """
    # 1. 获取当前时间
    if current_timestamp is None:
        now = datetime.now()
    elif isinstance(current_timestamp, datetime):
        now = current_timestamp
    else:
        raise TypeError("current_timestamp must be datetime object or None")
    
    # 2. 处理时区
    tz_info = now.tzinfo
    if tz_info is not None:
        if tz_offset is None:
            tz_offset = tz_info
    
    # 3. 设置默认时间
    hour = target_hour if target_hour is not None else 0
    minute = target_minute if target_minute is not None else 0
    second = target_second if target_second is not None else 0
    
    # 4. 验证时间参数
    if not (0 <= target_month <= 12):
        raise ValueError(f"target_month must be between 1 and 12, got {target_month}")
    if not (1 <= target_day <= 31):
        raise ValueError(f"target_day must be between 1 and 31, got {target_day}")
    if not (0 <= hour <= 23):
        raise ValueError(f"target_hour must be between 0 and 23, got {hour}")
    if not (0 <= minute <= 59):
        raise ValueError(f"target_minute must be between 0 and 59, got {minute}")
    if not (0 <= second <= 59):
        raise ValueError(f"target_second must be between 0 and 59, got {second}")
    
    # 5. 创建目标日期时间对象（处理闰年）
    current_year = now.year
    
    def create_target_datetime(year: int) -> datetime:
        """创建目标日期时间对象，处理闰年异常"""
        try:
            return datetime(
                year,
                target_month,
                target_day,
                hour,
                minute,
                second,
                tzinfo=tz_offset,
            )
        except ValueError:
            # 处理无效日期（如非闰年的2月29日）
            # 注意：这里根据业务需求可以有不同的处理方式
            if target_month == 2 and target_day == 29:
                # 方案1：改为3月1日
                return datetime(year, 3, 1, hour, minute, second, tzinfo=tz_offset)
            else:
                # 其他无效日期，抛出异常
                raise
    
    # 6. 创建今年的目标日期
    try:
        target_this_year = create_target_datetime(current_year)
    except ValueError as e:
        # 如果创建失败，尝试使用3月1日（仅当是2月29日的情况）
        if target_month == 2 and target_day == 29:
            target_this_year = datetime(current_year, 3, 1, hour, minute, second, tzinfo=tz_offset)
        else:
            raise ValueError(f"Invalid date: {target_month}/{target_day}") from e
    
    # 7. 计算目标年份
    # 判断逻辑：如果当前时间已经过了今年的目标时间，则计算到明年
    if now >= target_this_year:
        target_year = current_year + 1
    else:
        target_year = current_year
    
    # 8. 创建最终的目标日期
    try:
        target_date = create_target_datetime(target_year)
    except ValueError:
        if target_month == 2 and target_day == 29:
            target_date = datetime(target_year, 3, 1, hour, minute, second, tzinfo=tz_offset)
        else:
            raise
    
    # 9. 计算时间差
    time_left = target_date - now
    
    # 10. 安全保护：确保时间差不为负数
    # 如果因为某些原因计算出负数（如时区问题），则加一年
    if time_left.total_seconds() < 0:
        target_year += 1
        try:
            target_date = create_target_datetime(target_year)
        except ValueError:
            if target_month == 2 and target_day == 29:
                target_date = datetime(target_year, 3, 1, hour, minute, second, tzinfo=tz_offset)
            else:
                raise
        time_left = target_date - now
    
    return time_left
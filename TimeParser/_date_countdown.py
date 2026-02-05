from datetime import datetime, timedelta
from typing import Callable

def calculation_date_countdown(
        target_month:int,
        target_day:int,
        target_hour:int | None = None,
        target_minute:int | None = None,
        target_second:int | None = None,
    ) -> timedelta:
    """
    获取距离目标日期还有多少天
    """
    now = datetime.now()
    current_year = now.year
    
    try:
        # 尝试创建今年的日期（判断闰年兼容性）
        birthday_this_year = datetime(
            current_year,
            target_month,
            target_day,
            target_hour or 0,
            target_minute or 0,
            target_second or 0,
        )
    except ValueError:
        # 处理闰年日期（如2月29日，非闰年时调整为3月1日）
        birthday_this_year = datetime(current_year, 3, 1)
    
    # 判断当前是否在当天
    if now.date() == birthday_this_year.date():
        return timedelta()
    
    # 计算下一次的年份
    if now > birthday_this_year:
        next_year = current_year + 1
    else:
        next_year = current_year
    
    # 创建下一次的时间对象（精确到零点）
    try:
        next_birthday = datetime(next_year, target_month, target_day)
    except ValueError:
        next_birthday = datetime(next_year, 3, 1)
    
    # 计算时间差
    time_left = next_birthday - now
    
    # 处理时间差为负数的情况（确保逻辑正确）
    if time_left.total_seconds() < 0:
        next_birthday = datetime(next_year + 1, target_month, target_day)
        time_left = next_birthday - now
    
    return time_left
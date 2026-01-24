from datetime import datetime, timedelta
from typing import Callable

def get_birthday_countdown(
        birthday_month:int,
        birthday_day:int,
        name:str = "",
        time_format_func: Callable[[str, timedelta], str] = lambda name, td: f"And to {name}'s birthday: {td.days} days left",
        is_birthday_format_func: Callable[[str], str] = lambda name: f"Happy birthday to {name}!"
    ) -> str:
    """
    获取距离生日还有多少天
    """
    now = datetime.now()
    current_year = now.year
    
    try:
        # 尝试创建今年的生日日期（判断闰年兼容性）
        birthday_this_year = datetime(current_year, birthday_month, birthday_day)
    except ValueError:
        # 处理闰年生日（如2月29日，非闰年时调整为3月1日）
        birthday_this_year = datetime(current_year, 3, 1)
    
    # 判断当前是否在生日当天
    if now.date() == birthday_this_year.date():
        return is_birthday_format_func(name)
    
    # 计算下一次生日的年份
    if now > birthday_this_year:
        next_year = current_year + 1
    else:
        next_year = current_year
    
    # 创建下一次生日的时间对象（精确到零点）
    try:
        next_birthday = datetime(next_year, birthday_month, birthday_day)
    except ValueError:
        next_birthday = datetime(next_year, 3, 1)
    
    # 计算时间差
    time_left = next_birthday - now
    
    # 处理时间差为负数的情况（确保逻辑正确）
    if time_left.total_seconds() < 0:
        next_birthday = datetime(next_year + 1, birthday_month, birthday_day)
        time_left = next_birthday - now
    
    return time_format_func(name, time_left)
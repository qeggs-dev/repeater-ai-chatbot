# Date Countdown Function

提供日期倒计时功能

- `birthday_countdown`
  - Params:
    - `target_month` (int): 生日月份
    - `target_day` (int): 生日日期
    - `target_hour` (int): 生日小时
    - `target_minute` (int): 生日分钟
    - `target_second` (int): 生日秒数
    - `precise` (bool): 是否使用精确输出 (需要关闭 `time_delta_output`)
    - `time_delta_output` (bool): 是否输出 `datetime.timedelta` 对象
  - Returns:
    - (str | int): 
      - `str`: 倒计时字符串
      - `int`: 倒计时天数
# 模板变量表

| 变量 | 描述 | 参数 |
| :---: | :---: | :---: |
| `user_id` | 用户ID | 无 |
| `botname` | Bot名称 | 无 |
| `age` | 年龄 | 出生年份(Optional[int]) <br/> 出生月份(Optional[int]) <br/> 出生日期(Optional[int]) |
| `precise_age` | 精确年龄 | 出生年份(int) <br/> 出生月份(int) <br/> 出生日期(int) <br/> 出生小时(Optional[int]) <br/> 出生分钟(Optional[int]) <br/> 出生秒(Optional[int]) |
| `bot_birthday` | Bot生日 | 无 |
| `birthday_countdown` | 生日倒计时 | 生日月份(Optional[int]) <br/> 生日日期(Optional[int]) <br/> 寿星姓名(Optional[str]) <br/> 启用详细信息(Optional[bool]) |
| `zodiac` | 星座 | 出生月份(Optional[int]) <br/> 出生日期(Optional[int]) |
| `user_info` | 用户信息 | 无 |
| `user_name` | 用户名 | 无 |
| `nickname` | 用户昵称 | 无 |
| `user_age` | 用户年龄 | 无 |
| `model_uid` | 模型UID | 无 |
| `model_name` | 模型名称 | 无 |
| `model_type` | 模型类型 | 无 |
| `model_group` | 模型组 | 无 |
| `user_gender` | 用户性别 | 无 |
| `user_profile` | 用户资料 | 无 |
| `generate_uuid` | 生成UUID | 无 |
| `time` | 当前时间 | 格式字符串(Optional[str]) |
| `reprs` | 显示对象的字符串表示 | 任何内容(*Any) |
| `random` | 随机数 | 随机数下限(int) <br/> 随机数上下限(int) |
| `randfloat` | 随机浮点数 | 随机数下限(float) <br/> 随机数上下限(float) |
| `randchoice` | 随机选择 | 抽取内容(*str) |
| `copytext` | 重复文本 | 重复文本(str) <br/> 重复次数(int) <br/> 间隔符(Optional[str]) |
| `text_matrix` | 文本矩阵 | 重复文本(int) <br/> 列数(int) <br/> 行数(int) <br/> 间隔符(Optional[str]) <br/> 换行符(Optional[str]) |
| `random_matrix` | 0~1随机矩阵 | 矩阵行数(int) <br/> 矩阵列数(int) |
| `date_countdown` | 日期倒计时 | 目标月份(int) <br/> 目标日期(int) <br/> 日期名称(str) <br/> 启用详细信息(Optional[bool]) |
| `user_configs` | 用户配置 | 缩进(Optional[int]) <br/> 转义为ANSI(Optional[bool]) |
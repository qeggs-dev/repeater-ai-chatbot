# 模板变量表

| 变量 | 类型 | 描述 | 参数 |
| :---: | :---: | :---: | :---: |
| `version` | 字面量 | 版本 | 无 |
| `user_id` | 字面量 | 用户ID | 无 |
| `botname` | 字面量 | Bot名称 | 无 |
| `age` | 函数 | 年龄 | 出生年份(Optional[int]) <br/> 出生月份(Optional[int]) <br/> 出生日期(Optional[int]) |
| `precise_age` | 函数 | 精确年龄 | 出生年份(int) <br/> 出生月份(int) <br/> 出生日期(int) <br/> 出生小时(Optional[int]) <br/> 出生分钟(Optional[int]) <br/> 出生秒(Optional[int]) |
| `bot_birthday` | 字面量 | Bot生日 | 无 |
| `birthday_countdown` | 函数 | 生日倒计时 | 生日月份(Optional[int]) <br/> 生日日期(Optional[int]) <br/> 寿星姓名(Optional[str]) <br/> 启用详细信息(Optional[bool]) |
| `zodiac` | 函数 | 星座 | 出生月份(Optional[int]) <br/> 出生日期(Optional[int]) |
| `user_info` | 字面量 | 用户信息 | 无 |
| `username` | 字面量 | 用户名 | 无 |
| `nickname` | 字面量 | 用户昵称 | 无 |
| `user_age` | 字面量 | 用户年龄 | 无 |
| `user_gender` | 字面量 | 用户性别 | 无 |
| `model_uid` | 字面量 | 模型UID | 无 |
| `model_name` | 字面量 | 模型名称 | 无 |
| `model_type` | 字面量 | 模型类型 | 无 |
| `model_group` | 字面量 | 模型组 | 无 |
| `user_profile` | 字面量 | 用户资料 | 无 |
| `generate_uuid` | 函数 | 生成UUID | 无 |
| `time` | 函数 | 当前时间 | 格式字符串(Optional[str]) |
| `reprs` | 函数 | 显示对象的字符串表示 | 任何内容(*Any) |
| `random` | 函数 | 随机数 | 随机数下限(int) <br/> 随机数上下限(int) |
| `randfloat` | 函数 | 随机浮点数 | 随机数下限(float) <br/> 随机数上下限(float) |
| `randchoice` | 函数 | 随机选择 | 抽取内容(*str) |
| `copytext` | 函数 | 重复文本 | 重复文本(str) <br/> 重复次数(int) <br/> 间隔符(Optional[str]) |
| `text_matrix` | 函数 | 文本矩阵 | 重复文本(int) <br/> 列数(int) <br/> 行数(int) <br/> 间隔符(Optional[str]) <br/> 换行符(Optional[str]) |
| `random_matrix` | 函数 | 0~1随机矩阵 | 矩阵行数(int) <br/> 矩阵列数(int) |
| `date_countdown` | 函数 | 日期倒计时 | 目标月份(int) <br/> 目标日期(int) <br/> 日期名称(str) <br/> 启用详细信息(Optional[bool]) |
| `user_configs` | 函数 | 用户配置 | 缩进(Optional[int]) <br/> 转义为ANSI(Optional[bool]) |
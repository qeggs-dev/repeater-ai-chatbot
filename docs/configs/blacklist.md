# Blacklist 配置文件

该配置文件是一个 REGEX CHECKER 配置文件
详情请参考 [REGEX CHECKER 配置文件](regex_checker.md)

## 示例

```re
[REGEX PARALLEL FILE]
.*example_blacklist.*
```
这样，所有包含 `example_blacklist` 的请求都会被忽略
Repeater 会检查 `user_id`, `user_name`, `nick_name` 等字段
如果这些字段中包含 `example_blacklist`，则会主端口被拒绝响应

PS: 该处使用的正则匹配模式是 `search`
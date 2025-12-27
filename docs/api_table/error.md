# API Error

有时候，API 会出现一些问题，
某些 API 可能会有自己的特殊响应，
但如果这些错误未被正确处理，
那么它们就会被全局异常处理器捕获并记录日志。

如果此时服务器还能够正常返回数据
那么，API 响应的数据结构将如下：

- `error_message` 错误消息，该字段由配置定义，不包含什么详细信息
- `error_code` 错误码，通常为 `500`
- `source_exception` 源异常名称，比如 `ValueError`、`TypeError` 等
- `exception_message` 源异常消息，比如 `invalid literal for int() with base 10: 'abc'`
- `exception_traceback` 源异常的调用栈，通常该字段为隐藏状态，可以通过配置的方式启用
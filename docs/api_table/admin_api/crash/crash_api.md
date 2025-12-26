# Server Crash API

手动触发服务器最高级别崩溃，
主要用于调试目的

- **`/admin/crash`**
  - **method**: `POST`
  - **Header**
    - `X-Admin-API-Key (str)` API 密钥
  - **Response**
    - *\*服务器可能并不会返回一个有效的内容, 大概率会是`500 Internal Server Error`*

这么做会抛出一个`CRITICAL_EXCEPTION`，
这个异常会被全局捕获器捕获，
它会认为服务器出现了不可挽回的异常，
从而关闭服务器。
*(这可能会导致有些资源无法被正确释放)*

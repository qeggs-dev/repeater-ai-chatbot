# Server Raise Error API

手动抛出一些常见的异常
通常用于测试异常处理器

- **`/admin/crash`**
  - **method**: `POST`
  - **Header**
    - `X-Admin-API-Key (str)` API 密钥
  - **Request**
    - **type**: `JSON`
    - **Request Body**
      - `type (str)` 抛出的异常类型
      - `args (list)` 抛出异常时传递的参数
      - `kwargs (dict)` 抛出异常时传递的关键字参数
  - **Response**
    - *\*服务器可能并不会返回一个有效的内容, 大概率会是`500 Internal Server Error`*


# Server Raise Warning API

手动抛出一些常见的警告
通常用于测试全局异常处理器

- **`/admin/debug/raise_warning`**
  - **method**: `POST`
  - **Header**
    - `X-Admin-API-Key (str)` API 密钥
  - **Request**
    - **type**: `JSON`
    - **Request Body**
      - `type (str)` 抛出的警告名称
      - `message (str)` 抛出警告时使用的消息
  - **Response**
    - `warning (str)` 警告名称
    - `message (str)` 使用的消息
    

支持的警告名称：
  - `Warning`
  - `UserWarning`
  - `DeprecationWarning`
  - `PendingDeprecationWarning`
  - `SyntaxWarning`
  - `RuntimeWarning`
  - `FutureWarning`
  - `ImportWarning`
  - `UnicodeWarning`
  - `EncodingWarning`
  - `BytesWarning`
  - `ResourceWarning`
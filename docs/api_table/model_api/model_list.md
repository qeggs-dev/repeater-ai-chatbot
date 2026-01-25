# Model List

列出所有模型

- **`/model/list/{model_type: str}`**
  - **method**: `GET`
  - **Response**
    - **type:** `JSON`
    - **Response Body**
      - *\*List:*
        - `name(str)`: 模型名称
        - `url(str)`: 模型地址
        - `id(str)`: API方的模型ID
        - `parent(str)`: 所在组ID
        - `type(str)`: 模型类型
        - `timeout(int)`: 请求超时时间

模型类型请参考：
[模型类型](../../model_type.md)
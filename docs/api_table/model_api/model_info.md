# Model INFO

列出所有指定UID的模型

- **`/model/list/{model_type: str}/{model_uid: str}`**
  - **method**: `GET`
  - **Response**
    - **type:** `JSON`
    - **Response Body**
      - *\*Api INFO列表*

Api INFO 对象结构

API_INFO
- `name (str)` 模型名称
- `url (str)` 该模型所在的 URL
- `id (str)` 该模型在API中的ID
- `parent (str)` 该模型所属的组名称
- `uid (str)` 该模型的唯一标识符
- `type (str)` 该模型的模型类型
- `timeout (float)` 该模型请求的超时时间，单位为秒

虽然这里可以列出UID里所有的模型，
但在请求时，只有第一个模型才能被调用。
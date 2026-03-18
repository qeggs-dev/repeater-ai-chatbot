# Model List

列出所有模型

- **`/model/list/{model_type: str}`**
  - **method**: `GET`
  - **Response**
    - **type:** `JSON`
    - **Response Body**
          - `message` (str): 状态信息
          - `models` (list[[API_INFO](./api_info_obj.md)]): 模型列表

模型类型请参考：
[模型类型](../../model_type.md)
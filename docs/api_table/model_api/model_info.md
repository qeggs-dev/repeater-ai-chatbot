# Model INFO

列出所有指定UID的模型

- **`/models/{model_id: str}`**
  - **method**: `GET`
  - **Request**
    - **Query**
      - `detailed_info` (bool): 是否返回详细模型信息，默认为 False
  - **Response**
    - **type:** `JSON`
    - **Content:**
      - `message` (str): 状态信息
      - `models` (list[[API_INFO](./api_info_obj.md)]): 模型列表
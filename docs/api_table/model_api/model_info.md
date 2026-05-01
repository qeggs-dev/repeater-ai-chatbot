# Model INFO

列出所有指定UID的模型

- **`/models/{model_uid: str}`**
  - **method**: `GET`
  - **Response**
    - **type:** `JSON`
    - **Content:**
      - `message` (str): 状态信息
      - `models` (list[[API_INFO](./api_info_obj.md)]): 模型列表
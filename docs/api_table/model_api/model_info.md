# Model INFO

列出所有指定UID的模型

- **`/model/list/{model_type: str}/{model_uid: str}`**
  - **method**: `GET`
  - **Response**
    - **type:** `JSON`
    - **Response Body**
      - `message` (str): 状态信息
      - `models` (list[[API_INFO](./api_info_obj.md)]): 模型列表

虽然这里可以列出UID里所有的模型，
但在请求时，只有第一个模型才能被调用。
# Model INFO

列出所有指定UID的模型

- **`/model/list/{model_type: str}/{model_uid: str}`**
  - **method**: `GET`
  - **Response**
    - **type:** `JSON`
    - **Response Body**
      - `message` (str): 状态信息
      - `models` (list[[API_INFO](./api_info_obj.md)]): 模型列表

请求时如果 uid 上有多个模型
则随机一个模型开始请求。
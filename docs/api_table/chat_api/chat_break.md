# Break Chat Task API

用于打断当前所有提交的 Chat 任务

- **`/chat/break/{user_id:str}`**
  - **Request**
    - ***method:** `POST`
  - **Response**
    - `code` (int): HTTP 状态码
    - `msg` (str): API 返回的消息
    - `cancel_count` (int): 取消的任务数量
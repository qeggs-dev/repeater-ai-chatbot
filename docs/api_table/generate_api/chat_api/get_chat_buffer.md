# Get Chat Buffer API

查看当前生成任务的缓冲区内容

- **`/generate/chat/buffer/{user_id:str}`**
  - **Request**
    - ***method:** `GET`
  - **Response**
    - `user_id`
    - `buffers` (dict[str, dict[str, str]]): 缓冲区内容
      - *\*task_id* (str): 任务ID
        - `reasoning` (str): 推理内容
        - `content` (str): AI回复内容
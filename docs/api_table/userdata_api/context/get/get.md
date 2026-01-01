# Get Context API

从当前用户获取上下文信息

- **`/userdata/context/get/{user_id:str}`**
  - **Requset**
    - **method:** `GET`
  - **Response**
    - **type:** `JSON列表`
    - **Response Body**:
      - *\*参考[OpenAI Context](https://platform.openai.com/docs/api-reference/chat/create#chat_create-messages)*

获取当前用户所有上下文信息
注：这里头部并不会存放 `System Prompt`
它是单独存放并动态拼接的
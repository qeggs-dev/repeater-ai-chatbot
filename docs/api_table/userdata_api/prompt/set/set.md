# Set Prompt API

设置指定用户的提示词

- **`/userdata/prompt/set/{user_id:str}`**
  - **Requset**
    - **method:** `PUT`
    - **type:** `FORM`
    - **Request Body**:
      - `prompt (str)`: 提示词内容
  - **Response**
    - **type:** `Text`
    - **Response Body**:
      - "Prompt seted"

该提示词会在该用户对话时生效
如果为空则恢复为默认提示词
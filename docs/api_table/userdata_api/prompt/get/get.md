# Get Prompt API

从当前用户获取提示词内容

- **`/userdata/prompt/get/{user_id:str}`**
  - **Requset**
    - **method:** `GET`
  - **Response**
    - **type:** `Text`
    - **Response Body**:
      - *\*当前用户设置的提示词*

如果用户使用的是默认提示词
则返回的是一个空字符串
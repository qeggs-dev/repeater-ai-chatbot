# Variable Expand API

使用[变量展开引擎](../template_expansion_engine/main.md)
对用户数据进行变量展开
具体变量请参考[变量列表](../template_expansion_engine/variables.md)

- **`/variable_expand/{user_id:str}`**
  - **Requset**
    - **method:** `POST`
    - **type:** `JSON`
    - **Request Body**:
      - `user_info`
        - `username (str)` 用户名
        - `nickname (str)` 昵称
        - `age (int | float)` 年龄
        - `gender (str)` 性别
      - `text (str)` 要处理的文本
  - **Response**
    - **type:** `Text`
    - **Response Body**:
      - *\*处理后的文本*

注：使用该API时
模型相关的变量将为空

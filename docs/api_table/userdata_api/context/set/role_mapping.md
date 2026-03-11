# Context Role Mapping API

映射上下文角色到另一个角色，或按角色移除上下文单元

- **`/userdata/context/role_mapping/{user_id:str}`**
  - **Requset**
    - **method:** `POST`
    - **type:** `JSON`
    - **Request Body**:
      - (dict[str, str]): 角色映射表
  - **Response**
    - **type:** `JSON`
    - **Response Body**:
      - `status` (str): 状态码，如果 `http code` 为 `200` 则必为`success`
      - `context` (Context): 更新后的Context内容
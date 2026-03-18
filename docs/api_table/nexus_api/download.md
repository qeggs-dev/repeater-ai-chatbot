# Nexus Download API

从 Nexus 下载用户数据

- **`/nexus/download/{user_id:str}/single/{user_data_type:str}`**
  - **method**: `POST`
  - **Request**
    - **type:** `JSON`
    - **Request Body**
      - `id` (str): UUID 字符串
  - **Response**
    - **type:** `JSON`
    - **Response Body**
      - `message` (str): 响应信息
      - `nexus_message` (str): Nexus 响应信息

用户数据类型请查看 [User Data Type](./../userdata_api/user_data_type.md)
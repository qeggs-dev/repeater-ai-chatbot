# Nexus Upload API

上传用户数据到 Nexus

- **`/nexus/upload/{user_id:str}/single/{user_data_type:str}`**
  - **method**: `POST`
  - **Request**
    - **type:** `JSON`
    - **Content:**
      - `timeout` (int|float|null): 文件失效时间，默认为`None`，表示文件不会失效
  - **Response**
    - **type:** `JSON`
    - **Content:**
      - `message` (str): 响应信息
      - `nexus_message` (str): Nexus 响应信息
      - `resource_uuid` (str): 资源UUID

用户数据类型请查看 [User Data Type](./../userdata_api/user_data_type.md)
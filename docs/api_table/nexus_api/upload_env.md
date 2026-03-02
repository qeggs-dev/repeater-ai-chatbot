# Nexus Upload Environment API

上传一个用户环境到 Nexus

- **`/nexus/upload/{user_id:str}/environment`**
  - **method**: `POST`
  - **Request**
    - **type:** `JSON`
    - **Request Body**
      - `timeout` (int|float|null): 文件失效时间，默认为`None`，表示文件不会失效
  - **Response**
    - **type:** `JSON`
    - **Response Body**
      - `message` (str): 响应信息
      - `nexus_message` (str): Nexus 响应信息

上传用户环境就是
同时上传当前用户的三个数据类型
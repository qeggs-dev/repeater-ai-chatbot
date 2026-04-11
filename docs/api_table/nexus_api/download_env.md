# Nexus Download Environment API

从 Nexus 下载一个用户环境

- **`/nexus/download/{user_id:str}/environment`**
  - **method**: `POST`
  - **Request**
    - **type:** `JSON`
    - **Content:**
      - `id` (str): UUID 字符串
  - **Response**
    - **type:** `JSON`
    - **Content:**
      - `message` (str): 响应信息
      - `nexus_message` (str): Nexus 响应信息

下载用户环境就是
同时下载当前用户的三个数据类型
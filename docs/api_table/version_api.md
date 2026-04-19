# Version API

- **`/version`**
  - **Request**
    - **method:** `GET`
  - **Response**
    - **type:** `JSON`
    - **Content:**
      - `core` (str): 核心的版本号

此外，你也可以在路由上添加模块名来仅获取目标模块的版本信息
- **`/version/<module>`**
  - **Request**
    - **method:** `GET`
  - **Response**
    - **type:** `TEXT`
    - **Content:**
      - *\*目标模块的版本号*
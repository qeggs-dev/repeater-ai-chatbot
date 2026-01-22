# Get User File API

让服务器打包用户文件为ZIP
并返回给用户

- **`/userdata/file/{user_id:str}.zip`**
  - **Requset**
    - **method:** `GET`
  - **Response**
    - **type:** `File`
    - **Response Body**:
      - *\*用户数据ZIP文件*

该文件通常会包含以下文件
- `userfile.zip`
  - `raw`
    - `context.json` 用户上下文文件
    - `prompt.json` 用户提示文件
    - `user_config.json` 用户配置文件
  - `readable`
    - `context.txt` 用户上下文文件（可读格式）
    - `prompt.txt` 用户提示文件（纯文本格式）
    - `user_config.yaml` 用户配置文件（YAML格式）
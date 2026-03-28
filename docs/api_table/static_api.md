# Static API

- **`/static/{path}`**
  - **Request**
    - **method:** `GET`
    - **Query**:
      - `text_encoding` (str): 文本编码，不填则以文件方式发送
  - **Response**
    - **type:** `Static File` or `Text`
# Core Task Status API

用于监控主请求任务状态

- **`/status/core/task/{user_id}`**
  - **Request**
    - **method**: `GET`
  - **Response**
    - **type**: `JSON List`
    - **Response Body**
      - *\*当前执行阶段的任务栈列表*

目前的结构如下:
- `Tasking`
  - `Prepareing`
  - `Requesting`
  - `PostProcessing`
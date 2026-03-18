# Core Task Status API

用于监控主请求任务状态

- **`/status/core/task/{user_id}`**
  - **Request**
    - **method**: `GET`
  - **Response**
    - **type**: `JSON List`
    - **Response Body**
      - *\*当前执行阶段的任务栈列表*

目前任务结构树如下:

**非流式：**
- `Tasking`
  - `Prepareing`
    - `Checking Blacklist`
    - `Getting Config`
    - `Processing Cross User Data Access`
    - `Getting model`
    - `Mapping user name`
    - `Getting template parser`
    - `Processing context`
      - `Getting history context`
      - `Role mapping`
      - `Checking request contains only text`
      - `Splicing user input`
      - `Shrinking context`
    - `Make Request Object`
    - `Pre-filled output`
  - `Requesting`
    - `Init objects`
    - `Create OpenAI Client`
    - `Write calling log base data`
    - `Check context`
    - `Make extra body`
      - `thinking`
    - `Send Request`
    - `Processing Response`
    - `Logging Response Content`
    - `Fast Statistics`
  - `PostProcessing`
    - `Template Expanding`
    - `Saving Context`
    - `Recording request log`
    - `Returning response`

**流式：**
- `Tasking`
  - `Prepareing`
    - `Checking Blacklist`
    - `Getting Config`
    - `Processing Cross User Data Access`
    - `Getting model`
    - `Mapping user name`
    - `Getting template parser`
    - `Processing context`
      - `Getting history context`
      - `Role mapping`
      - `Checking request contains only text`
      - `Splicing user input`
      - `Shrinking context`
    - `Make Request Object`
    - `Pre-filled output`
  - `Requesting`
    - `Create OpenAI Client`
    - `Write calling log base data`
    - `Check context`
    - `Make extra body`
      - `thinking`
    - `Streaming`
    - `Logging Response Content`
    - `Fast Statistics`
  - `PostProcessing`
    - `Template Expanding`
    - `Saving Context`
    - `Recording request log`
    - `Returning response`
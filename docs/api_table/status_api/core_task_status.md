# Core Task Status API

用于监控主请求任务状态

- **`/status/core/task/{user_id}`**
  - **Request**
    - **method**: `GET`
  - **Response**
    - **type**: `JSON`
    - **Content:**
      - `contains` (bool): 当前用户是否存在任务
      - `tasks` (dict[str, list[str]]): 每个 task_id 对应的执行栈状态
      - *\*List*
      

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
      - `Check Multimodal Message`
      - `Splicing user input`
      - `Shrinking context`
    - `Make Request Object`
    - `Make Request Runtime Object`
    - `Pre-filled output`
    - `Pre-filled Model Response`
  - `Requesting`
    - `Init objects`
    - `Create OpenAI Client`
    - `Write calling log base data`
    - `Check context`
    - `Make extra body`
      - `thinking`
      - `reasoning_effort`
      - `user_id`
    - `Send Request`
    - `Processing Response`
    - `Logging Response Content`
    - `Fast Statistics`
  - `Calling Tools`
  - `PostProcessing`
    - `Template Expanding`
    - `Saving Context`
    - `Recording request log`
    - `Returning response`

**流式：**
- `Tasking`
  - `Prepareing`
    - `Checking Blacklist`
    - `Processing Cross User Data Access`
    - `Getting model`
    - `Mapping user name`
    - `Getting template parser`
    - `Processing context`
      - `Getting history context`
      - `Role mapping`
      - `Check Multimodal Message`
      - `Splicing user input`
      - `Shrinking context`
    - `Make Request Object`
    - `Make Request Runtime Object`
    - `Pre-filled output`
    - `Pre-filled Model Response`
  - `Requesting`
    - `Create OpenAI Client`
    - `Write calling log base data`
    - `Check context`
    - `Make extra body`
      - `thinking`
      - `reasoning_effort`
      - `user_id`
    - `Streaming`
    - `Logging Response Content`
    - `Fast Statistics`
  - `Calling Tools`
  - `PostProcessing`
    - `Template Expanding`
    - `Saving Context`
    - `Recording request log`
    - `Returning response`
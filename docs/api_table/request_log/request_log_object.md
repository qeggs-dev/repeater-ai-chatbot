# Request Log Object

## Fields
  - `id (str)` 请求的唯一标识符
  - `url (str)` 请求的目标URL
  - `model (str)` 请求的模型ID
  - `user_id (str)` 请求的用户ID
  - `user_name (str | null)` 请求的用户名
  - `stream (bool)` 是否启用了流式响应
  - `total_chunk (int)` 请求的总 Chunk 数量
  - `empty_chunk (int)` 请求的空 Chunk 数量
  - `task_start_time (TimeStamp)` 任务开始时间
  - `prepare _start_time (TimeStamp)` 预处理开始时间
  - `prepare _end_time (TimeStamp)` 预处理结束时间
  - `request_start_time (TimeStamp)` 请求开始时间
  - `request_end_time (TimeStamp)` 请求结束时间
  - `stream_processing_start_time (TimeStamp)` 流式处理开始时间
  - `stream_processing_end_time (TimeStamp)` 流式处理结束时间
  - `task_end_time (TimeStamp)` 任务结束时间
  - `chunk_times (list[TimeStamp])` Chunk 时间列表
  - `created_time (int)` API报告的创建时间
  - `total_tokens (int)` 请求的总 Token 数量
  - `prompt_tokens (int)` 输入的 Token 数量
  - `completion_tokens (int)` 生成的 Token 数量
  - `cache_hit_count (int)` 缓存命中的 Token 数量
  - `cache_miss_count (int)` 缓存未命中的 Token 数量
  - `total_context_length (int)` 请求结束后的总上下文字符数
  - `reasoning_content_length (int)` 生成的 CoT 文本长度
  - `new_content_length (int)` 请求结束后的新上下文的单元数量

## TimeStamp

`TimeStamp` 是一个包含两个时间戳的数据结构，用于记录时间。
其有如下属性：

- `timestamp (int)` 时间戳
- `monotonic (int)` 单调时间戳

用于对各个关键点进行时间记录，
方便后续进行性能分析。

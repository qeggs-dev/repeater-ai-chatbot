# Withdraw Context API

从当前用户Context中删除最后一组对话

- **`/userdata/context/get/{user_id:str}`**
  - **Requset**
    - **method:** `POST`
    - **type:** `FORM`
    - **Request Body**:
      - `context_pair_num (int)` 删除的组数
  - **Response**
    - **type:** `JSON`
    - **Response Body**:
      - `status (str)` 状态码，如果 `http code` 为 `200` 则必为`success`
      - `deleted (int)` 删除的上下文单元数量
      - `deleted_context (Context)` 删除的上下文内容
      - `delete_context_pair (int)` 删除的上下文组数量
      - `context (Context)` 剩余的上下文内容

注：该API默认以一对上下文单元为单位进行删除
也就是
在删除掉结尾多余的User后
向上删除非User单元直到再次遇到User单元
并继续删除User单元直到遇到非User单元
当前 Context Pair 删除结束，开始删除下一个 Context Pair

举例：
```json
[
  {
    "role": "user",
    "content": "Please communicate with me in brief language"
  },
  {
    "role": "assistant",
    "content": "Got it.  \nAsk short, get short.  \nWhat do you need?"
  },
  {
    "role": "user",
    "content": "Hello, which is bigger, 0.8 or 0.11."
  },
  {
    "role": "assistant",
    "content": "Yes.  \n\n0.999… = 1 exactly.  \nIt’s a limit; the infinite 9’s reach 1.  \nProof:  \nLet \\( x = 0.999... \\)  \n\\( 10x = 9.999... \\)  \nSubtract: \\( 9x = 9 \\) → \\( x = 1 \\)."
  },
  {
    "role": "user",
    "content": "Also, 0.999.. Equals 1?"
  },
  {
    "role": "assistant",
    "content": "Yes.\n\n0.999… = 1. Exactly equal. Not approximate.\n\nReason: Infinite decimals represent limits.  \n0.999… = 9/9 = 1."
  }
]
```

提交 `context_pair_num = 1` 的请求后，Context 数据将会变成：
```json
[
  {
    "role": "user",
    "content": "Please communicate with me in brief language"
  },
  {
    "role": "assistant",
    "content": "Got it.  \nAsk short, get short.  \nWhat do you need?"
  },
  {
    "role": "user",
    "content": "Hello, which is bigger, 0.8 or 0.11."
  },
  {
    "role": "assistant",
    "content": "Yes.  \n\n0.999… = 1 exactly.  \nIt’s a limit; the infinite 9’s reach 1.  \nProof:  \nLet \\( x = 0.999... \\)  \n\\( 10x = 9.999... \\)  \nSubtract: \\( 9x = 9 \\) → \\( x = 1 \\)."
  }
]
```